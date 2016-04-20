'''
Created on Mar 29, 2016

@author: iitow
'''
import os
import optparse
from terminal import shell,rsync,ssh

this_dir = os.path.dirname(os.path.realpath(__file__))
package_path = this_dir.rsplit('/',1)[0]
artifact_path = this_dir.rsplit('/',2)[0]

def menu():
    parser = optparse.OptionParser()
    parser.add_option(
                    '-b',
                    '--build',
                    default="isi-fog_0.1_all.deb",
                    help="build name"),
    parser.add_option(
                    '-f', '--server',
                    default="es-fog-dev.west.isilon.com",
                    help="Your fog server instance ip or dns name"),
    parser.add_option(
                      '-d',
                      '--docs',
                      action ='store_false',
                       dest="docs",
                       default=True,
                       help="Add sphinx docs to package")
    (opts, _) = parser.parse_args()
    return opts

def make_package(options):
    if options.docs:
        shell("cd %s/docs; sphinx-apidoc -f -o source/ ../isi_fog_py" % (package_path))
        shell("cd %s/docs; make html" % (package_path))
        shell("cd %s; tar -zcvf isi_fog_py.tar.gz ./isi_fog_py" % (package_path))
    shell("cd %s; dpkg-buildpackage -rfakeroot -Tclean" % (package_path))
    shell("cd %s; dpkg-buildpackage -b" % (package_path))
    server = options.server
    src = "%s/%s" % (artifact_path,options.build)
    dest = "/root"
    print "server: %s" % server
    print "   src: %s" % src
    print "  dest: %s" % dest
    rsync(server,src,dest,rsa_private="~/.ssh/id_rsa",option='push')
    ssh(server,"cd /root; gdebi %s -n" % (options.build),rsa_private="~/.ssh/id_rsa")
    
    
    


if __name__ == '__main__':
    options = menu()
    print options
    make_package(options)
    
    