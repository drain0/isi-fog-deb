'''
Created on Jun 2, 2015

:author: iitow
'''
import os
import requests
import json
from requests.auth import HTTPBasicAuth
from requests import Request, Session



class Restful(object):
    def __init__(self,base_url,auth_file=None,debug=False):
        '''Generic class to handle All types of Restful requests and basic authentication
        
        :param base_url: fully qualified path to api path example:https://github.west.isilon.com/api/v3
        :param auth_file: a yaml file containing user: <username> password: <password>
        '''
        self.debug    = debug
        self.user     = None
        self.password = None
        self.set_auth = False
        if auth_file:
            try:
                import yaml
                with open(auth_file, 'r') as file:
                    auth = yaml.load(file)    
            except:
                print "[Error] Using auth_file at path <%s>" % (auth_file)
                os.sys.exit(1)
            self.user = auth.get('user')
            self.password =auth.get('password')
            self.set_auth = True 
        self.base_url = base_url
        self.session = Session()
    def send(self,rest_action,url_ext,data=None,strict=False,Content_Type='application/json',verify=False):
        '''Generic call to handle all types of restful requests
        
        :param rest_action: Possible option, 'GET','PUT','POST','PATCH'
        :param url_ext: added to base url example https://github.west.isilon.com/<url_ext>
        :param strict: False, will permit errors as warning & return code, True will exit with code
        :param Content_Type: How info is formed, example application/xml  
        :param verify: Check for Certificates 
        :return: String of content, or error exit code
        '''
        auth = None
        if self.set_auth:### set auth parameters if defined
            auth = HTTPBasicAuth(self.user,self.password)
        if 'json' in Content_Type:
            data = json.dumps(data)
        full_url = "%s/%s" % (self.base_url,url_ext)
        headers = {'Content-Type': Content_Type} ### set headers 
        request_handle = Request(rest_action, ### request handle
                                 full_url,
                                 headers=headers,
                                 data=data,
                                 auth=auth).prepare()
        response = self.session.send(request_handle,verify=verify)
        if self.debug:
            print ("\n [%s] %s \n %s") % (rest_action,full_url,response)
        status = response.status_code
        if 200 == status:
            return response.content### returns content as string
        else:
            print "[strict %s] Request was not successful [code] %s" % (strict,status)
            if strict:
                print "[exit code] %s" % (status)
                os.sys.exit(response.status_code)
            return status
        
    def post_multipart(self,url_ext,data=None,files=None,strict=True):
        full_url = "%s/%s" % (self.base_url,url_ext)
        response = requests.post(full_url,data=data,files=files)
        print ("\n [%s] %s \n %s") % ('post_multipart',full_url,response)
        status = response.status_code
        if 200 == status:
            return response.content### returns content as string
        else:
            print "[strict %s] Request was not successful [code] %s" % (strict,status)
            if strict:
                print "[exit code] %s" % (status)
                os.sys.exit(response.status_code)
            return status
        
if __name__ == '__main__':
    pass
    ''' Basic usage example
    url_ext = 'user'
    branch   = 'BR_IITOW_SVN_BRANCH'
    revision = '206'
    server   = "https://github.west.isilon.com/api/v3" 
    url_ext = "user"
    com = Restful(server,auth_file='auth.yaml')
    print com.send('GET', url_ext)
    '''
    
    