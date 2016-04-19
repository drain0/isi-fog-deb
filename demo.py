'''
Created on Apr 14, 2016

@author: iitow
'''
import argparse
import json
import sys
import time
from py_module.terminal import shell

def menu():
    parser = argparse.ArgumentParser(
        description='Demo isilon api fog')
    parser.add_argument('--one',
                        action="store_true",
                        dest="one",
                        default=False,
                        help='Add several nodes')
    
    parser.add_argument('--two',
                        action="store_true",
                        dest="two",
                        default=False,
                        help='Remove several nodes')
    
    parser.add_argument('--three',
                        action="store_true",
                        dest="three",
                        default=False,
                        help='Configure Node')
    
    parser.add_argument('--four',
                        action="store_true",
                        dest="four",
                        default=False,
                        help='Reimage Node')
    return parser.parse_args()

def one(nodes):
    for node in range(0,nodes):
        hostname = "node_%02d" % (node)
        mac = "00:00:00:00:00:%02d" % (node)
        print "%s : %s" % (hostname, mac)
        shell('python py_module/fog-cli.py -c isi_register_host -V \'{"hostname":"%s","mac":"%s"}\'' % (hostname,mac))

def two(nodes):
    for node in range(0,nodes):
        hostname = "node_%02d" % (node)
        mac = "00:00:00:00:00:%02d" % (node)
        print "%s : %s" % (hostname, mac)
        shell('python py_module/fog-cli.py -c isi_destroy_host -V "hostname=%s"' % (hostname))

def three():    
    # Register host
    shell('python py_module/fog-cli.py -c isi_register_host -V \'{"hostname":"%s","mac":"%s"}\'' % (hostname,mac))
    # Configure Host
    shell('python py_module/fog-cli.py -c isi_set_host_kernel -V \'{"hostname":"%s","kernel_path":"%s"}\'' % (hostname,kernel))
    shell('python py_module/fog-cli.py -c isi_set_host_kernel_args -V \'{"hostname":"%s","kernel_args":"%s"}\'' % (hostname,kernel_args))
    shell('python py_module/fog-cli.py -c isi_set_host_description -V \'{"hostname":"%s","description":"%s"}\'' % (hostname,description))

def four():
    
    #Add node to queue
    shell('python py_module/fog-cli.py -c isi_queue_host -V \'{"hostname":"%s","taskTypeID":"%s"}\'' % (hostname,25))
    #Reboot the node
    shell('python py_module/fog-cli.py -c isi_ipmi_reset -V \'{"user":"%s","password":"%s","ip":"%s"}\'' % (user,password,ipmi_ip))
    # make sure the node has started imaging check state
    output = shell('python py_module/fog-cli.py -c isi_get_host_state -V \'{"hostname":"%s"}\'' % 
                   (hostname),verbose=False).get('stdout')
    output = _sanitize(output)
    output = json.loads(output,encoding='utf-8')    
    state = output.get('stdout').get('state')
    if not state == 1:
        print "Error node is not queued state %s" % state
        sys.exit(1)
    _wizard_check()

def _wizard_check():
    cnt = 0
    timeout = 300
    print "Waiting for node to img sleep 7.5 minutes"
    time.sleep(450)
    # monitor for node being finished 
    for ping in range(0,timeout):
        print " ping @ %s" % (str(ping))
        try:
            output = shell('python py_module/fog-cli.py -c isi_get_host_state -V \'{"hostname":"%s"}\'' % (hostname),strict=False).get('stdout')
            output = _sanitize(output)
            output = json.loads(output,encoding='utf-8') 
            state = output.get('stdout').get('state')
        except Exception as e:
            print str(e)
            state=1
        print "state @ %s" % (state)
        if state==0:
            print "Node finished imaging"
            break
        if cnt >= timeout-1:
            print "error node timeout occurred"
            sys.exit(1)
        cnt+=1
        time.sleep(1)
    # check serial of node for the wizard
    _serial = serial.split(':')
    cnt=0
    for ping in range(0,timeout):
        print " ping @ %s" % (str(ping))
        output = shell('python py_module/fog-cli.py -c isi_telnet_cmd -V \'{"host":"%s","port":"%s"}\'' % (_serial[0],_serial[1])).get('stdout')
        if 'wizard' in output.lower():
            print "##########################"
            print "WIZARD FOUND"
            print "##########################"
            break
        
        if cnt >= timeout-1:
            print "error node timeout occurred"
            sys.exit(1)
        cnt+=1
        time.sleep(1)

def _sanitize(str):
    str = str.replace(", u'",", '").replace("{u'","{'").replace(": u'",": '").replace("'",'"')
    return str.strip()
        
if __name__ == '__main__':
    # ipmi settings
    ipmi_ip='10.7.169.145'
    user='ADMIN'
    password='ADMIN'
    
    # Node Settings
    hostname = 'WF784'
    mac='00:25:90:62:13:24'
    serial='cs628.west.isilon.com:8030'
    build='http://buildbiox.west.isilon.com/snapshots/b.8.0.0.037/RELEASES/latest/OneFS_v8.0.0.1_Install.tar.gz'
    #build="http://buildbiox.west.isilon.com/releases/release-7.1.1.9/OneFS_v7.1.1.9_Install.tar.gz"
    kernel='http://buildbiox.west.isilon.com/snapshots/b.8.0.0.037/RELEASES/latest/OneFS_v8.0.0.1_reimg.img.gz'
    kernel_args='force=True,pxe=True,state=4,build=%s' % (build)
    description='ipmi_ip=%s\nserial=%s' % (ipmi_ip,serial)
    
    options = menu()
    nodes = 30
    if options.one:
        one(nodes)
    if options.two:
        two(nodes)
    if options.three:
        three()
    if options.four:
        four()
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
    