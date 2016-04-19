from pyVmomi import vim
from pyVim import connect
import atexit
import optparse
import json

def menu():
    p = optparse.OptionParser(description='reboots virtual machine esxi',
                                        prog='isi_vm_reboot',
                                        version='1.0',
                                        usage= "usage: %prog  ")
    p.add_option('-n' ,'--hostname' ,action ='store', type="string", dest="name", default="" ,help="provide the hostname")
    p.add_option('-v' ,'--vmhost' ,action ='store', type="string", dest="vmhost", default=["vcenter02.prod.sea1.west.isilon.com","eng-mgt-vcenter.west.isilon.com"] ,help="provide the hostname")
    p.add_option('-u' ,'--user' ,action ='store', type="string", dest="user", default="SVC-SEA.EngJenkinsSt" ,help="vm host user")
    p.add_option('-p' ,'--password' ,action ='store', type="string", dest="password", default="" ,help="vm host password")
    (options,args) = p.parse_args()
    options = options.__dict__
    return options

def reboot(service_instance,name):
    content = service_instance.content
    objView = content.viewManager.CreateContainerView(content.rootFolder,
                                                        [vim.VirtualMachine],
                                                        True)
    vmList = objView.view
    objView.Destroy()
    vm=None
    for v in vmList:
        if v.name == name:
            vm=v
    if vm:
        summary = vm.summary
        TASK = vm.ResetVM_Task()
        return True
    return False

def read_config():
    with open('/var/www/fog/commons/isi_vm_reboot.json') as data_file:    
        data = json.load(data_file)
        return data

def connection(host,user,password):
    try:
        service_instance = connect.SmartConnect(host=host,user=user,pwd=password,port=443)
        return service_instance
    except Exception as e:
        print str(e)
    atexit.register(connect.Disconnect, service_instance)
if __name__ == "__main__":
    options = menu()
    user    = options.get('user')
    password= options.get('password')
    name    = options.get('name')
    for host in options.get('vmhost'):
        service_instance = connection(host,user,password)
        if reboot(service_instance,name):
            print 'True'
            break      