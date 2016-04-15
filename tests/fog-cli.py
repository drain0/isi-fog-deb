'''
Created on Apr 14, 2016

@author: iitow
'''
import argparse
import json
from http import Restful

def menu():
    parser = argparse.ArgumentParser(
        description='Isilon api changes in fog')
    parser.add_argument('-s',
                        action="store",
                        dest="server",
                        default='http://es-fog-dev.west.isilon.com/fog',
                        help='http base url example: http://es-fog-dev.west.isilon.com/fog')
    parser.add_argument('-a',
                        action="store_true",
                        dest="api",
                        default=False,
                        help='print a list of all restful api end points')
    parser.add_argument('-c',
                        action="store",
                        dest="cmd",
                        default='isi_get_hosts',
                        help='based on the commands list in the api at {url}/fog/service/api.json select command')
    parser.add_argument('-V',
                        action="store",
                        dest="variables",
                        default='',
                        help='add variables in the form of key1=value1 key2=value2 --note: space is the delimiter')
    parser.add_argument('-d',
                        action="store_true",
                        dest="debug",
                        default=False,
                        help='print additional debug info')
    parser.add_argument('--version',
                        action='version',
                        version='%(prog)s 1.0')
    return parser.parse_args()

def get_api(options,session):
    ext = 'service/api.json'
    output = session.send('GET',ext)
    output = json.loads(output)
    if options.debug or options.api:
        print ''
        for cmd, url in output.iteritems():
            print "  %s\n -- %s\n" % (cmd,url)
    return output

def run(options,session,api):
    vars = ''
    if api.get(options.cmd):
        variables = options.variables.split(' ')
        for var in variables:
            vars = "%s&%s" % (vars,var)
        api_url = api.get(options.cmd).get('url').split('fog',1)[1].split('?',1)[0]
        print api_url
        ext = '%s?%s' % (api_url,vars)
        output = session.send('GET',ext)
        output = json.loads(output)
        if options.debug:
            print output
        return output
    else:
        print "[Error] cmd not found %s " % (options.cmd)
        print "try [-a] to print api list"

if __name__ == '__main__':
    options = menu()
    if options.debug:
        print options
    session = Restful(options.server)
    api = get_api(options, session)
    print run(options, session, api)
    