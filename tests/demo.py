'''
Created on Apr 14, 2016

@author: iitow
'''
import argparse
from terminal import shell

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
        shell('python fog-cli.py -c isi_register_host -V "hostname=%s mac=%s"' % (hostname,mac))

def two(nodes):
    for node in range(0,nodes):
        hostname = "node_%02d" % (node)
        mac = "00:00:00:00:00:%02d" % (node)
        print "%s : %s" % (hostname, mac)
        shell('python fog-cli.py -c isi_destroy_host -V "hostname=%s"' % (hostname))

def three():
    # settings to configure
    hostname = 'WF784'
    mac='00:25:90:62:13:24'
    ipmi_ip='10.7.169.145'
    serial='cs628:8030'
    build='http://buildbiox.west.isilon.com/snapshots/b.8.0.0.037/RELEASES/latest/OneFS_v8.0.0.1_Install.tar.gz'
    kernel='http://buildbiox.west.isilon.com/snapshots/b.8.0.0.037/RELEASES/latest/OneFS_v8.0.0.1_reimg.img.gz'
    kernel_args='force=True,pxe=True,state=4,build=%s' % (build)
    description='ipmi_ip=%s\nserial=%s' % (ipmi_ip,serial)
    # Register host
    shell('python fog-cli.py -c isi_register_host -V "hostname=%s mac=%s"' % (hostname,mac))
    # Configure Host
    shell('python fog-cli.py -c isi_set_host_kernel -V "hostname=%s kernel_path=%s"' % (hostname,kernel))
    shell('python fog-cli.py -c isi_set_host_kernel_args -V "hostname=%s kernel_args=%s"' % (hostname,kernel_args))
    shell('python fog-cli.py -c isi_set_host_description -V "hostname=%s description=%s"' % (hostname,description))

def four():
    #Add node to queue
    shell('python fog-cli.py -c isi_queue_host -V "hostname=%s taskTypeID=%s"' % (hostname,25))
    
    
    
    
    

if __name__ == '__main__':
    options = menu()
    nodes = 30
    if options.one:
        one(nodes)
    if options.two:
        two(nodes)
    if options.three:
        three()
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
    