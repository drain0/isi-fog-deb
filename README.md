### prerequisites ###
* Only compatible with fog 1.3.0
* Must install Fog before using this package
* Do not set a password for mysql leave it blank.

### Package Creation ###
* dpkg-buildpackage -b 
* dpkg-buildpackage -rfakeroot -Tclean 

### Package installation ###
* apt-get install gdebi-core --tested @ 0.9.5.3ubuntu2
* apt-get install python-pip --tested @ 1.5.4-1ubuntu3
* apt-get install ipmitool   --tested @ 1.8.13-1ubuntu0.6
* pip install pyvmomi==5.5.0-2014.1.1 
* pip install pyvim          --tested @ 0.0.16
* sudo gdebi isi-fog_0.1_all.deb
* goto /var/www/fog/service/isi_vm_reboot.py input host_1,host_2,user,password
