'''
Created on Apr 18, 2016

@author: iitow
'''
from fog import Api

class BareMetal(object):
    ''' This class is specific to Isilon bare-metal provisioning
    '''
    def __init__(self, url, debug=False):
        ''' Init BareMetal object
        @param url: base url of fog server example: http://es-fog-dev.west.isilon.com/fog
        @param debug: print out all info 
        '''
        self.debug = debug
        self.url = url
        self.session = Api(self.url,debug=self.debug)
        self.api = self._get_api()

''' Example. '''
if __name__ == '__main__':
    url = 'http://es-fog-dev.west.isilon.com/fog'
    session = Api(url)
    output = session.send('isi_get_hosts',test='hello',test2='hello2')
    print output
        