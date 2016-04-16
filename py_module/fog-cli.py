'''
Created on Apr 14, 2016

@author: iitow
'''
import argparse
import json
from fog import Api


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
                        default='{}',
                        type=json.loads,
                        help='add variables in the form of \'{"mac":"00:00:00:00:00:00\"}\' '),
    parser.add_argument('-d',
                        action="store_true",
                        dest="debug",
                        default=False,
                        help='print additional debug info')
    parser.add_argument('--version',
                        action='version',
                        version='%(prog)s 1.0')
    return parser.parse_args()


def run(options):
    server = options.server
    cmd = options.cmd
    variables = options.variables
    debug = options.debug
    session = Api(server,debug=debug)
    if options.api:
        session.print_api()
    else:
        print session.send(cmd,**variables)
    
    
if __name__ == '__main__':
    options = menu()
    run(options)
    