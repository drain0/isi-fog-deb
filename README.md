* Only compatible with fog 1.3.0
* Must install Fog before using this package
* Do not set a password for mysql leave it blank.

### Package Creation ###
* dpkg-buildpackage -b 
* dpkg-buildpackage -rfakeroot -Tclean 

### Package installation ###
* apt-get install gdebi-core
* apt-get install python-pip
* pip install pyvmomi 
* sudo gdebi isi-fog_0.1_all.deb
* goto /var/www/fog/service/isi_vm_reboot.py input host_1,host_2,user,password
