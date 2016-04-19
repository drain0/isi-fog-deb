'''
Created on Mar 30, 2016

@author: iitow
'''
import os
import optparse
import sys
import telnetlib
import time

class TelnetCmd(object):
    def __init__(self,host,port,timeout=1,debug=False):
        self.host = host
        self.port = port
        self.timeout = timeout
        self.session = None
        self.debug = debug
        self.has_session = self.connect()
    def __del__(self):
        if self.debug:
            print "closing session"
        self.session.close()
    
    def connect(self):
        cnt = 0
        while True:
            cnt+=1
            status =  self._connect()
            if self.debug:
                print "Connect attempt @ %s" % (cnt)
                print "status: %s" % status
            if status:
                return True
            if cnt >= self.timeout:
                print "Unable to connect %s:%s" % (self.host,self.port)
                sys.exit(1)
            time.sleep(1)
        return False

    def _connect(self):
        try:
            self.session = telnetlib.Telnet()
            self.session.open(self.host,self.port)
            output = self.session.read_until('', 1)
            if self.debug:
                print output
            return True
        except Exception as e:
            print str(e)
            return False
    
    def write(self,cmd,match,timeout=3):
        if self.has_session:
            try:
                cmd = "%s\n" % cmd
                self.session.write(cmd)
                output = self.session.read_until(match, timeout)
                #print output
                return output
                self.session.close()
            except Exception as e:
                print e
        else:
            print "[Error] Session not available"

def menu():
    p = optparse.OptionParser(description='Telnet session single command',
                                        prog='isi_telnet_cmd',
                                        version='1.0',
                                        usage= "usage: %prog  ")
    p.add_option('-H' ,'--host' ,action ='store', type="string", dest="host", default="" ,help="hostname")
    p.add_option('-p' ,'--port' ,action ='store', type="string", dest="port", default="" ,help="port number")
    p.add_option('-c' ,'--cmd' ,action ='store', type="string", dest="cmd", default="\n" ,help="command to execute")
    p.add_option('-m' ,'--match' ,action ='store', type="string", dest="match", default="#" ,help="end telnet read on a matched word")
    p.add_option('-d' ,'--debug' ,action ='store_true', dest="debug", default=False ,help="print all debug output")
    (options,args) = p.parse_args()
    options = options.__dict__
    for key,value in options.iteritems():
        if not value and not key=='debug':
            print "[Error] missing --%s" % key
            sys.exit(1)
    return options
        
if __name__ == '__main__':
    options = menu()
    com = TelnetCmd(options.get('host'),options.get('port'),debug=options.get('debug'))
    print com.write(options.get('cmd'), options.get('match'))
    
    #host = 'cs628'
    #port = '8030'
    #com = TelnetCmd(host,port)
    #cmd = ''
    #match = 'Wizard'
    #timeout = 3
    #output = com.write(cmd, match)
    #if 'Wizard' in output:
    #    print "WIZARD FOUND"
        
        
        
        
        
        
        
        
        
        
