'''
Created on Apr 18, 2016

@author: iitow
'''
from fog import Api
import sys

class Onefs(Api):
    ''' This class is specific to Isilon bare-metal provisioning for onefs
    @note: see fog.py for additional info
    '''
    def __init__(self, url, debug=True):
        ''' Init BareMetal object
        @param url: base url of fog server example: http://es-fog-dev.west.isilon.com/fog
        @param debug: print out all info 
        '''
        Api.__init__(self,url,debug=debug)

    def register_host(self,hostname,mac,kernel_path,kernel_args,**description):
        ''' Creates a fog host and updates info
        @param hostname: string, hostname
        @param mac: string, mac address
        @param kernel_path: string, http path to kernel on buildbiox
        @param kernel_args: string, kernel arguments to be passed to fog host
        @param description: add key value pairs to description in the form of key=value/n 
        @return: boolean, Success
        @note: Here to check if updates occured @ http://<UrFogServer>/fog/management/?node=host
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
        output = self.send('isi_destroy_host',hostname=hostname)
        if not output.get('code') == 0:
            print '[Error] %s' % output.get('stderr')
            return False
        return True
    
    def reboot_host(self,host,type,**args):
        ''' Reboot a node
        @param host: String, Service you wish to use to reboot hostname/ip
        @param type: pdu,ipmi,vm 
        @param **args: additional args to accomplish tasks
        '''
        if type.lower()=='pdu':
            print "[Error] PDU reset not implemented"
            return False
        elif type.lower()=='vm': 
            if not args.get('user') or not args.get('password'):
                print "[Error] ipmi needs ip,user,password values ", args
            else:
                output = self.send('isi_vm_reboot',hostname=host,user=args.get('user'),password=args.get('password'))
                if not output.get('code') == 0:
                    print '[Error] %s' % output.get('stderr')
                    return False
        elif type.lower()=='ipmi': 
            if not args.get('user') or not args.get('password'):
                print "[Error] ipmi needs user,password values ", args
                return False
            else:
                output = self.send('isi_ipmi_reset',ip=host,user=args.get('user'),password=args.get('password'))
                if not output.get('code') == 0:
                    print '[Error] %s' % output.get('stderr')
                    return False
        else:
            print "[Error] type not found %s" % (type)
            return False
        return True

    def queue_host(self,hostname,taskTypeID=25):
        ''' Add host to the queue to be re-imged
        @param hostname: string, name of system
        @return: boolean Success 
        '''
        output = self.send('isi_queue_host',hostname=hostname,taskTypeID=taskTypeID)
        if not output.get('code') == 0:
            print '[Error] %s' % output.get('stderr')
            return False
        return True

    def reimg_node(self,hostname,mac,**kwargs):
        ''' reimg a Onefs node
        @param hostname: name of Onefs system
        @param kwargs: additional args to be added  
        @return: boolean Successful
        @note: This can be changed to include different reboot options in the future
        '''
        pass

''' Example.'''
if __name__ == '__main__':
    url = 'http://es-fog-dev.west.isilon.com/fog'
    hostname = 'test1'
    mac = '00:00:00:00:00:00'
    kernel_path = 'http://buildbiox.west.isilon.com/snapshots/b.8.0.0.037/RELEASES/latest/OneFS_v8.0.0.1_reimg.img.gz'
    kernel_args = 'force=True,pxe=True,state=4,build=http://buildbiox.west.isilon.com/snapshots/b.8.0.0.037/RELEASES/latest/OneFS_v8.0.0.1_Install.tar.gz'
    
    session = Onefs(url)
    session.register_host(hostname,mac,kernel_path,kernel_args,hello='world',test='1')
    #session.destroy_host(hostname)
    #session.queue_host(hostname)




























        