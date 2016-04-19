'''
Created on Apr 18, 2016

@author: iitow
'''
import optparse
import time
from isi_telnet_cmd import TelnetCmd

def menu():
    p = optparse.OptionParser(description='pdu reboot',
                                        prog='isi_pdu_reboot',
                                        version='1.0',
                                        usage= "usage: %prog  ")
    p.add_option('-i' ,'--ip' ,action ='store', type="string", dest="ip", default="" ,help="host server ip address")
    p.add_option('-u' ,'--user' ,action ='store', type="string", dest="user", default="admn" ,help="host username")
    p.add_option('-p' ,'--password' ,action ='store', type="string", dest="password", default="admn" ,help="host password")
    p.add_option('-o' ,'--outlet' ,action ='store', type="string", dest="outlet" ,help="outlet to restart")
    (options,args) = p.parse_args()
    options = options.__dict__
    return options

def reboot(options):
    com = TelnetCmd(options.get('ip'),'23')
    com.write(options.get('user'),'Username:')
    com.write(options.get('password'),'Password:')
    com.write('REBOOT','Switched CDU:')
    com.write(options.get('outlet'),'   Outlet or Group Name:')
    output = com.write('','   Command successful')
    if "Command successful" in output:
        return True
    return False

if __name__ == '__main__':
    options = menu()
    cnt = 0
    timeout = 3
    while True:
        if reboot(options):
            print 'True'
            break
        cnt+=1
        time.sleep(1)
        if cnt >= 3:
            print 'False'
            break