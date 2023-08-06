from .qing import qing,GET,POST
from .qiu import qiu
from .tools import tools
from .gl import getGlobal,setGlobal


from .transform import curl_to_request_kwargs
from .help import help_pytest_cmd,help_vscode_config

true=True
false=False
null=None

'''
demo

class aaa(qing):
    method='get'
    scheme='https'
    host='xxxx.com'
    path='/asdasd/asdasd'
    headers={}
    body=''
    auth=('xxx','xxxx')
    timeout=3 #second
    params='xxxx&xxxx'
    url='' #可以包含 scheme host path params

    def xxx(self):
        self.request()
or

class bbb:
    method='get'
    scheme='https'
    host='xxxx.com'
    path='/asdasd/asdasd'
    headers={}
    body=''
    auth=('xxx','xxxx')
    timeout=3 #second
    params='xxxx&xxxx'
    url='' #可以包含 scheme host path params

    def xxx(self):
        qing(self).request()

or

qing().setURL('').request()

'''

