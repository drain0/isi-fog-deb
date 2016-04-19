'''
Created on Apr 15, 2016

:author: iitow
'''
import json
import sys
from http import Restful

class Api(object):
    '''This is a generic class for communication with fog server
    
    '''
    def __init__(self, url, debug=False):
        '''Init fog object
        
        :param url: base url of fog server example: http://es-fog-dev.west.isilon.com/fog
        :param debug: print out all info 
        '''
        self.debug = debug
        self.url = url
        self.session = Restful(self.url,debug=self.debug)
        self.api = self._get_api()

    def _get_api(self):
        '''Get the active api list
        
        :return: dict api from {url}/fog/service/api.json
        '''
        ext = 'service/api.json'
        output = self.session.send('GET',ext)
        if type(output) is int:
            print {'stderr':'unreachable','stdout':'','stdin':'','code':output}
            sys.exit(output)          
        output = json.loads(output)
        return output

    def print_api(self):
        ''' Prints api list out pretty
        '''
        print 'api list:'
        for cmd,args in self.api.iteritems():
            variables = ','.join(args.get('variables'))
            print "  [cmd] %s [Variables] %s" % (cmd.rjust(25),variables)

    def send(self,cmd,**kwargs):
        '''Generic http 'GET' with some error handling
        
        :param cmd: command from {url}/fog/service/isi_get_hosts.php
        :param **kwargs: any number of key=value pairs which form ?var1=val2&var2=val2....
        :return: dict {'stdout':'','stdin':'','stderr':'',code:0,} 
        '''
        if self.api.get(cmd):
            ext = self.api.get(cmd).get('ext')
            args_str = '?'
            cnt = 0
            for key,value in kwargs.iteritems():
                arg = '%s=%s' % (key,value)
                if cnt <= 0:
                    args_str = '%s%s' % (args_str,arg)
                else:
                    args_str = '%s&%s' % (args_str,arg)
                cnt+=1
            ext = '%s%s' % (ext,args_str)
            try:
                output = self.session.send('GET',ext)
                output = json.loads(output)
                return output
            except:
                pass
        else:
            print '[Error] cmd %s not found.' % (cmd)
            self.print_api()
        return None
''' Example.
if __name__ == '__main__':
    url = 'http://es-fog-dev.west.isilon.com/fog'
    session = Api(url)
    output = session.send('isi_get_hosts',test='hello',test2='hello2')
    print output
'''    