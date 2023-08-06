# -*- coding: UTF-8 -*-

from urllib.parse import urlparse
import requests
import logging
import urllib3
import os
import sys
import pytest

base_dir = os.path.dirname(__file__)
sys.path.append(base_dir)  # 临时修改环境变量
base_dir = os.path.dirname(base_dir)
sys.path.append(base_dir)
sys.path.append(os.getcwd())
sys.path.append(os.path.dirname(os.getcwd()))

from .qiu import qiu

from .gl import gData


urllib3.disable_warnings()
# tools.getfile()

log = logging.getLogger('')
logging.basicConfig(level=logging.INFO)
log.setLevel(logging.INFO)

# format_str = logging.Formatter('%(asctime)s\n%(message)s\n')
# sh = logging.StreamHandler()
# sh.setFormatter(format_str)
# log.addHandler(sh)


class qing(object):
    """
    """
    def __find_attr(self, this,k:dict, name, default=""):
        if name in dir(self):
            if self.__getattribute__(name) is not None:
                return self.__getattribute__(name)
            else:
                return default
        if this is not None and name in dir(this):
            if this.__getattribute__(name) is not None:
                return this.__getattribute__(name)
            else:
                return default
        if len(k)>0 and name in k:
            if k[name] is not None:
                return k[name]
            else:
                return default
        return default

    def __initParam(self):
        self.__backup = {'method': self.__method, 'scheme': self.__scheme, 'host': self.__host, 'path': self.__path,
                         'params_dict': self.__params_dict, 'headers': self.__headers, 'body': self.__body, 'auth': self.__auth, 'timeout': self.__timeout}
        self.__method = self.__backup['method']
        self.__scheme = self.__backup['scheme']
        self.__host = self.__backup['host']
        self.__path = self.__backup['path']
        self.__params_dict = self.__backup['params_dict']
        self.__headers = self.__backup['headers']
        self.__body = self.__backup['body']
        self.__auth = self.__backup['auth']
        self.__timeout = self.__backup['timeout']

    

    @staticmethod
    def skipIf(condition:bool,msg:str):
        if condition:
            pytest.skip(str(msg))

    def noLog(self,status=True):
        self.__nolog = status
        return self

    def POST(self, url=None,body=None,headers=None,params=None):
        self.GET(url,params=params,headers=headers)
        self.__method = 'post'
        if body is not None:
            self.setBody(body)
        self.__backup = {'method': self.__method, 'scheme': self.__scheme, 'host': self.__host, 'path': self.__path,
                         'params_dict': self.__params_dict, 'headers': self.__headers, 'body': self.__body, 'auth': self.__auth, 'timeout': self.__timeout}
        return self

    def GET(self, url=None,params=None,headers=None):
        self.__method = 'get'
        if url is not None:
            self.setURL(str(url))
        if params is not None:
            self.setParamDict(params)
        if headers is not None:
            if isinstance(headers,str):
                self.setHeaderString(headers)
            elif isinstance(headers,dict):
                self.setHeaders(headers)
        
        self.__backup = {'method': self.__method, 'scheme': self.__scheme, 'host': self.__host, 'path': self.__path,
                         'params_dict': self.__params_dict, 'headers': self.__headers, 'body': self.__body, 'auth': self.__auth, 'timeout': self.__timeout}

        return self

    def __init__(self, this=None,**k) -> None:
        '''
        参数名：ren
        method:get
        scheme:https
        host:
        path:
        headers:{}
        body:
        auth:None
        timeout:5
        params:
        url:
        '''
        self.__name = str(self.__find_attr(this,k, 'name', ""))
        self.__method = str(self.__find_attr(this,k, 'method', ""))
        self.__scheme = str(self.__find_attr(this,k, 'scheme', "https"))
        self.__host = str(self.__find_attr(this,k, 'host'))
        self.__path = str(self.__find_attr(this,k, 'path'))
        self.__params_dict = {}
        self.__func = None
        self.__nolog = False
        self.__funcargs = []
        self.__proxy={'http':None,"https":None}
        self.__headers = dict(self.__find_attr(this,k, 'headers', {}))
        self.__body = self.__find_attr(this,k, 'body')
        self.__body = self.__find_attr(this,k, 'data')
        self.__auth = self.__find_attr(this,k, 'auth', None)
        self.__isMultipart = False
        if isinstance(self.__auth, list) or isinstance(self.__auth, tuple):
            if len(self.__auth) == 2:
                self.setAuth(self.__auth[0], self.__auth[1])
            else:
                raise Exception("auth is err:"+str(self.__auth))
        else:
            if self.__auth is not None:
                raise Exception("auth is err:"+str(self.__auth))

        self.__timeout = float(self.__find_attr(this,k, 'timeout', 5))
        param = self.__find_attr(this,k, 'params')
        if isinstance(param, dict):
            self.__params_dict = dict(param)
        else:
            if str(param).startswith('?'):
                self.setParamStr(str(param)[1:])
            else:
                self.setParamStr(str(param))
        self.setURL(self.__find_attr(this,k, 'url'))
        self.__backup = {'method': self.__method, 'scheme': self.__scheme, 'host': self.__host, 'path': self.__path,
                         'params_dict': self.__params_dict, 'headers': self.__headers, 'body': self.__body, 'auth': self.__auth, 'timeout': self.__timeout}

    def setMethod(self, method: str):
        self.__method = method
        return self

    def setURL(self, url: str):
        # if url != '' and not self.__noWarn:
        #     log.warning("不推荐直接使用URL,建议使用具体的参数")
        u = urlparse(url)
        if len(self.__scheme) == 0:
            self.__scheme = u.scheme
        if len(self.__host) == 0:
            self.__host = u.netloc
        if len(self.__path) == 0:
            self.__path = u.path
        if len(self.__params_dict) == 0 and len(u.query) > 0:
            for key in u.query.split("&"):
                val = key.split("=")
                if len(val) == 2:
                    self.__params_dict[str(val[0])] = str(val[1])
                else:
                    self.warn("param解析错误：",key)
        return self
    
    def setHost(self,host:str):
        self.__host=str(host)
        return self
    
    def setPath(self,path:str):
        self.__path=str(path)
        return self

    @staticmethod
    def debug(*msg:str,sep=" "):
        if len(msg)>0:
            msg=[str(x) for x in msg]
            log.debug(str(sep).join(msg))

    @staticmethod
    def info(*msg:str,sep=" "):
        if len(msg)>0:
            msg=[str(x) for x in msg]

            log.info(str(sep).join(msg))

    @staticmethod
    def warn(*msg:str,sep=" "):
        if len(msg)>0:
            msg=[str(x) for x in msg]

            log.warning(str(sep).join(msg))

    @staticmethod
    def error(*msg:str,sep=" "):
        if len(msg)>0:
            msg=[str(x) for x in msg]
            log.error(str(sep).join(msg))

    @property
    def __PARAMS(self) -> str:
        tmp = ""
        for k in self.__params_dict:
            if k is None:
                continue
            tmp += str(k)+"="+str(self.__params_dict[k])+"&"
        if len(tmp) > 0:
            tmp = '?'+tmp[:-1]
        return tmp

    @property
    def URL(self) -> str:
        if self.__host == "":
            raise Exception("没有指定host")
        if self.__scheme == "":
            raise Exception("没有指定请求的协议（http/https）")
        return self.__scheme+"://" + self.__host+self.__path+self.__PARAMS


    def setBeforeFunc(self, func, *args):
        '''
        func: def func(val:qing,*args)
        
        '''
        self.__func = func
        self.__funcargs = list(args)
        return self


    def getParam(self, key: str) -> str:
        val = self.__params_dict.get(key)
        if val is None:
            raise Exception(key+"：请求参数无此值")
        else:
            return str(val)

    def setParam(self, key: str, val: str):
        if val is None and key in self.__params_dict:
            del self.__params_dict[key]
        else:
            self.__params_dict[str(key)] = str(val)
        return self

    def setParamStr(self, pa: str):
        if len(pa) > 0:
            for key in pa.split("&"):
                val = key.split("=")
                if len(val) == 2:
                    self.__params_dict[str(val[0])] = str(val[1])
        return self

    def setParamDict(self,pa:dict):
        if pa is not None:
            for k,v in pa.items():
                self.setParam(k,v)

    def setBody(self, body):
        self.__body = body
        return self

    def setContentTypeJson(self):
        self.__headers['content-type'] = "application/json; charset=utf-8"
        return self

    def setContenttypeKV(self):

        self.__headers['content-type'] = "application/x-www-form-urlencoded;charset=utf-8"
        return self

    def setContenttypeMultipart(self):
        self.__method = "POST"
        self.__isMultipart = True
        return self

    def setHeader(self, key: str, val: str):
        if val is None and key in self.__headers:
            del self.__headers[str(key).lower()]
        else:
            self.__headers[str(key).lower()] = str(val)
        return self
    
    def setHeaderString(self,headers:str):
        headers=headers.replace('\r','').split('\n')
        for h in headers:
            h2=h.split(': ')
            if len(h2)==2:
                self.__headers[str(h2[0])]=str(h2[1])
        return self

    def setHeaders(self, ddd: dict):
        
        self.__headers.update(ddd)
        return self

    def setName(self,name:str):
        self.__name=str(name)
        return self

    def setTimeout(self, timeout: float):
        """_summary_

        Args:
            timeout (int): 秒级参数

        Returns:
            _type_: 继续点下去
        """

        try:
            self.__timeout = float(timeout)
        except:
            pass
        return self

    def setAuth(self, user: str, passwd: str):
        self.__auth = (str(user), str(passwd))
        return self

    

    def setHttpProxy(self,http:str =None,https:str =None):
        self.__proxy['http']=str(http)
        self.__proxy['https']=str(https)


    def request(self):
        
        urllib3.disable_warnings()
        try:
            if self.__func is not None:
                if len(self.__funcargs) > 0:
                    self.func(self,*self.__funcargs)
                else:
                    self.__func(self)

            showStr = "\n----------------{}----------------\n".format(self.__name)
            showStr += self.__method+"\n"+self.URL+"\n"

            if len(self.__headers) > 0:
                headers = {}
                for k, v in self.__headers.items():

                    headers[str(k)] = str(v)
                    if not self.__isMultipart:
                        showStr += str(k)+": "+str(v)+"\n"
                self.__headers = headers.copy()
            if self.__method.lower() == "post" and self.__body != "" and not self.__isMultipart:
                showStr += str(self.__body)
            if not self.__nolog and not self.__isMultipart:
                log.info(showStr)
            
        except Exception as e:
            raise e
        try:
            if self.__isMultipart:
                if isinstance(self.__body, dict):
                    tmpdict = {}
                    for k, v in self.__body.items():
                        if isinstance(v, int) or isinstance(v, str) or isinstance(v, float):
                            tmpdict[k] = (None, str(v))
                        else:
                            tmpdict[k] = v
                    self.__body = tmpdict
                r = requests.request(self.__method, self.URL, headers=self.__headers, verify=False,
                                     allow_redirects=False, auth=self.__auth, files=self.__body, timeout=self.__timeout,proxies=self.__proxy)
                
                for k, v in r.request.headers.items():
                    showStr += str(k)+": "+str(v)+"\n"
                line = ""
                for l in str(r.request.body).split('\\r\\n'):
                    if len(l) < 100:
                        line += l+'\n'
                    else:
                        line += l[:100]+"...\n"
                showStr += line
                log.info(showStr)

            else:
                if self.__method=="":
                    if 'content-type' in self.__headers:
                        self.__method="post"
                    else:
                        self.__method="get"
                if isinstance(self.__body,str):
                    self.__body=self.__body.encode()
                r = requests.request(self.__method, self.URL, headers=self.__headers, verify=False,
                                     allow_redirects=False, auth=self.__auth, data=self.__body, timeout=self.__timeout,proxies=self.__proxy)
            try:
                self.res = qiu(r, log, self.__nolog,self.__name)
            except Exception as e:
                log.error('响应解析出错')
                raise e
            return self.res
        except Exception as e:
            raise e
        finally:
            self.__initParam()


def GET(url,params=None,headers=None):
    return qing().GET(url,params,headers)

def POST(url,body,headers):
    return qing().POST(url,body,headers)

    
