'''
Created on Apr 18, 2016

:author: iitow
'''
from fog import Api
import sys
import time

class Onefs(Api):
    ''' 
    This class is specific to Isilon bare-metal provisioning for onefs using fog
    
    :note: see fog.py for additional info
    :note: https://fogproject.org/
    :note: https://github.west.isilon.com/eng-tools/isi-fog-deb
    '''
    def __init__(self, url, debug=True):
        '''Init BareMetal object
        
        :param url: base url of fog server example: http://es-fog-dev.west.isilon.com/fog
        :param debug: print out all info 
        '''
        Api.__init__(self,url,debug=debug)

    def register_host(self,hostname,mac,kernel_path,kernel_args,**description):
        ''' 
        Creates a fog host and updates info
        
        :param hostname: string, hostname
        :param mac: string, mac address
        :param kernel_path: string, http path to kernel on buildbiox
        :param kernel_args: string, kernel arguments to be passed to fog host
        :param description: add key value pairs to description in the form of key=value/n 
        :return: boolean, Success
        :note: Here to check if updates occured @ http://<UrFogServer>/fog/management/?node=host
        '''
        output = self.send('isi_register_host',hostname=hostname,mac=mac)
        if not output.get('code') == 0:
            print '[Error] %s' % output.get('stderr')
            return False
        output = self.send('isi_set_host_kernel',hostname=hostname,kernel_path=kernel_path)
        if not output.get('code') == 0:
            print '[Error] %s' % output.get('stderr')
            return False
        output = self.send('isi_set_host_kernel_args',hostname=hostname,kernel_args=kernel_args)
        if not output.get('code') == 0:
            print '[Error] %s' % output.get('stderr')
            return False
        desc = ''
        for key,value in description.iteritems():
            desc = "%s%s=%s\n" % (desc,key,value)
        output = self.send('isi_set_host_description',hostname=hostname,description=desc)
        if not output.get('code') == 0:
            print '[Error] %s' % output.get('stderr')
            return False
        return True

    def destroy_host(self,hostname):
        ''' Destroy a host
        
        :param hostname: string, fog host
        :return: boolean, Success
        '''
        output = self.send('isi_destroy_host',hostname=hostname)
        if not output.get('code') == 0:
            print '[Error] %s' % output.get('stderr')
            return False
        return True
    
    def reboot_host(self,**Variables):
        ''' Reboot a node
        
        :param host: String, Service you wish to use to reboot hostname/ip
        :param **Variables: see 'isi_pdu_reboot','isi_vm_reboot','isi_ipmi_reset', : http://{url}/fog/service/api.json
        .. :note: example usage:
        ipmi - reboot_host(ip='192.168.1.1',user='ADMIN',password='ADMIN')
        pdu  - reboot_host(ip='192.168.1.1',user='ADMIN',password='ADMIN',outlet='.A16')
        vm   - reboot_host(hostname='SOMEVMNAME',user='ADMIN',password='ADMIN')
        '''
        if Variables.has_key('ip') and Variables.has_key('outlet'):
            print "PDU Reboot"
            output = self.send('isi_pdu_reboot',ip=Variables.get(ip),user=Variables.get('user'),password=Variables.get('password'),outlet=Variables.get('outlet'))
            if not output.get('code') == 0:
                print '[Error] %s' % output.get('stderr')
                return False
        elif Variables.has_key('hostname'): 
            print "VM Reboot"
            output = self.send('isi_vm_reboot',hostname=hostname,ip=ip,user=Variables.get('user'),password=Variables.get('password'))
            if not output.get('code') == 0:
                print '[Error] %s' % output.get('stderr')
                return False
        elif Variables.has_key('ip'): 
            print "IPMI Reboot"
            output = self.send('isi_ipmi_reset',ip=Variables.get('ip'),user=Variables.get('user'),password=Variables.get('password'))
            if not output.get('code') == 0:
                print '[Error] %s' % output.get('stderr')
                return False
        else:
            print "[Error] type not found %s" % (type)
            return False
        return True

    def queue_host(self,hostname,taskTypeID=25):
        '''Add host to the queue to be re-imged
        
        :param hostname: string, name of system
        :param taskTypeID: 
        :return: boolean Success 
        '''
        output = self.send('isi_queue_host',hostname=hostname,taskTypeID=taskTypeID)
        if not output.get('code') == 0:
            print '[Error] %s' % output.get('stderr')
            return False
        return True
    
    def dequeue_host(self,mac,state='4'):
        '''Add host to the queue to be re-imged
        
        :param mac: string, host mac
        :param state: string, 1-5
        :return: boolean Success 
        '''
        output = self.send('isi_set_host_state',mac=mac,state=state)
        if not output.get('code') == 0:
            print '[Error] %s' % output.get('stderr')
            return False
        return True
    
    def telnet_search(self,**Variables):
        """search telnet for specific values
        
        :param **variables: see 'isi_telnet_cmd' @ http://{url}/fog/service/api.json
        """
        print Variables
        for t in range(0,Variables.get('timeout')):
            output = self.send('isi_telnet_cmd',host=Variables.get('host'),port=Variables.get('port'))
            print output
            if output.get('code') >= 1:
                print output.get('stderr')
            if Variables.get('search').lower() in output.get('stdout').lower():
                print "[search] '%s' found" % (Variables.get('search'))
                return True
            if t > timeout-1:
                print "[Warning] timeout @ %s" % Variables.get('timeout')
            time.sleep(5)
        return False
    
    def img_node(self,hostname,**Variables):
        '''reimg a Onefs node
        
        :param hostname: name of Onefs system
        :param **Variables: see 'isi_telnet_cmd','isi_queue_host', @ http://{url}/fog/service/api.json
        :return: boolean, Success
        '''
        if Variables.has_key('timeout'):
            timeout = Variables.get('timeout')
        else:
            Variables['timeout']=400
        if not self.queue_host(hostname):
            print "[Error] unable to queue host"
            return False
        if not self.reboot_host(**Variables):
            print "[Error] unable to boot ", Variables
            return False
        hold = timeout*2
        print "Waiting for node to perform imaging %s sec" % (hold)
        time.sleep(hold)
        if Variables.get('search'):
            self.telnet_search(**Variables)
            return True
        return True

''' Example.'''
if __name__ == '__main__':
    url = 'http://es-fog-dev.west.isilon.com/fog'
    hostname = 'WF784'
    mac = '00:25:90:62:13:24'
    kernel_path = 'http://buildbiox.west.isilon.com/snapshots/b.8.0.0.037/RELEASES/latest/OneFS_v8.0.0.1_reimg.img.gz'
    kernel_args = 'force=True,pxe=True,state=4,build=http://buildbiox.west.isilon.com/snapshots/b.8.0.0.037/RELEASES/latest/OneFS_v8.0.0.1_Install.tar.gz'
    ip = "10.7.169.145"
    user = "ADMIN"
    password = "ADMIN"
    host = "cs628.west.isilon.com"
    port = "8030"
    timeout = 400
    search = 'wizard'
    
    session = Onefs(url)
    session.img_node(hostname,ip=ip,user=user,password=password,timeout=timeout,host=host,port=port,search=search)
    #session.register_host(hostname,mac,kernel_path,kernel_args,hello='world',test='1')
    #session.destroy_host(hostname)
    #session.queue_host(hostname)
    #print session.reboot_host(ip='10.7.169.145',user='ADMIN',password='ADMIN')





























        