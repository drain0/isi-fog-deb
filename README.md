package setup:
dpkg-buildpackage -b 
dpkg-buildpackage -rfakeroot -Tclean 

package usage:
sudo gdebi hive_0.1_all.deb 
