'''
Created on Mar 29, 2016

@author: iitow
'''
import optparse
from terminal import shell

def menu():
    p = optparse.OptionParser(description='ipmi reset',
                                        prog='isi_ipmi_reset',
                                        version='1.0',
                                        usage= "usage: %prog  ")
    p.add_option('-i' ,'--ip' ,action ='store', type="string", dest="ip", default="" ,help="bmc server ip address")
    p.add_option('-u' ,'--user' ,action ='store', type="string", dest="user", default="ADMIN" ,help="bmc username")
    p.add_option('-p' ,'--password' ,action ='store', type="string", dest="password", default="ADMIN" ,help="bmc password")
    (options,args) = p.parse_args()
    options = options.__dict__
    return options

def reset(options):
    ip = options.get('ip')
    user = options.get('user')
    password = options.get('password')
    cmd = 'ipmitool -I lanplus -H %s -U %s -P %s power reset' % (ip,user,password)
    session = shell(cmd)
    return session
    

if __name__ == '__main__':
    options = menu()
    output = reset(options)
    if 'Reset\n' in output.get('stdout'):
        print "True"
    else:
        print "False"