'''
Created on Apr 14, 2016

@author: iitow
'''
import argparse
import json
import sys
import time
from isi_fog_py.isilon import Onefs

def menu():
    parser = argparse.ArgumentParser(
        description='Demo isilon api fog')
    parser.add_argument('--img',
                        action="store_true",
                        dest="img",
                        default=False,
                        help='Add several nodes')
    
    return parser.parse_args()
        
if __name__ == '__main__':
    options = menu()
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
    if options.img:
        session = Onefs(url)
        session.img_node(hostname,ip=ip,user=user,password=password,timeout=timeout,host=host,port=port,search=search)

        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
    