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
    p.add_option('-n' ,'--name' ,action ='store', type="string", dest="name", default="" ,help="provide the hostname")
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
    
    print vm
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
    config = read_config()
    host_1  = config.get('host_1')
    host_2  = config.get('host_2')
    user    = config.get('user')
    password= config.get('password')
    options = menu()
    name    = options.get('name')
    service_instance = connection(host_1,user,password)
    if not reboot(service_instance,name):
        service_instance = connection(host_2,user,password)
        if not reboot(service_instance,name):
            print "false"
        else:
            print "true"