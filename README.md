* Only compatible with fog 1.3.0
* Must install Fog before using this package
* Do not set a password for mysql leave it blank.

### Package Creation ###
package setup:
dpkg-buildpackage -b 
dpkg-buildpackage -rfakeroot -Tclean 

### Package installation ###
package usage:
sudo gdebi isi-fog_0.1_all.deb
