# -*- coding: UTF-8 -*-
import json
import logging
import os
import sys

import requests
base_dir = os.path.dirname(__file__)
sys.path.append(base_dir)  # 临时修改环境变量
base_dir = os.path.dirname(base_dir)
sys.path.append(base_dir)
sys.path.append(os.getcwd())
sys.path.append(os.path.dirname(os.getcwd()))

from .check import Result,check, method,empty, optional




class qiu(object):
    def __init__(self, res: requests.Response, log=None, nolog=False,name='') -> None:
        '''
        res:requests.Response 响应结果
        log，日志类
        nolog：是否展示日志
        '''
        if log is None:
            self.log = logging.getLogger(__name__)
            self.log.setLevel(logging.DEBUG)
  
        else:
            self.log = log
        self.nolog = nolog
        self.__res = res
        self.msg = ""
        self.header = {}
        self.contentType = ""
        self.text = ""
        self.isJson = False
        self.json = {}
        self.CHECK=check
        self.result=""
        self.reqinfo=""
        self.name=name
        self.timeCost=int(res.elapsed.microseconds/1000)
        if res is not None and isinstance(res, requests.Response):
            self.result  += "耗时:"+str(int(res.elapsed.microseconds/1000))+"ms\n"
            self.result += str(self.__res.status_code)+" "+self.__res.reason+"\n"
            self.code = 0
            for k, v in res.headers.items():
                self.header[k] = v
                self.result += str(k)+": "+str(v)+"\n"
                if str(k).lower() == "content-type":
                    self.contentType = str(v)
                if self.contentType.lower().startswith("application/json"):
                    self.json = res.json()
                    self.isJson = True
                else:
                    try:
                        self.json = json.loads(res.text)
                        self.isJson = True
                    except: 
                        pass
            self.text = res.content.decode('utf-8')
            if '\\u' in self.text:
                try:
                    self.text = res.content.decode('unicode_escape')
                except:
                    pass
            self.result  += self.text+"\n"
            
            if not self.nolog:
                self.log.info("\n"+self.result)
            req=res.request
            self.reqinfo+=req.method+'\n'
            self.reqinfo+=req.url+'\n'
            for k,v in req.headers.items():
                 self.reqinfo += str(k)+": "+str(v)+"\n"
            if req.body is not None:
                if isinstance(req.body,bytes):
                    self.reqinfo+=req.body.decode()
                else:
                    self.reqinfo+=str(req.body)
        else:
            self.code = 1
            self.msg = str(res)
            self.result="err "+self.msg
            raise Exception(self.msg)




    def checkStatusCode(self, code: int,noException=False):
        try:
            if self.code == 0:
                if self.__res.status_code != int(code):
                    self.code = 2
                    self.msg = "响应状态码不正确，期望：{}，实际：{}".format(
                        code, self.__res.status_code)
                    raise Exception(self.msg)
            else:
                raise Exception(self.msg)
            return True,''
        except Exception as e:
            if noException:
                return False,str(e)
            else:
                raise e



    def checkValue(self,res:bool,msg=''):
        if not res:
            raise Exception("校验出现错误："+str(msg))

    def checkHeader(self, key: str, val:str,noException=False):
        try:
            if self.code == 0:
                if self.__res.headers.get(str(key)) is None:
                    raise Exception("不存在header:"+key)
                if val is not None:
                    if self.__res.headers.get(str(key)) != str(val):
                        raise Exception("header的值不正确,期望是:{}，实际是:{}".format(
                            val, self.__res.headers.get(str(key))))
            else:
                raise Exception(self.msg)
            return True,''
        except Exception as e:
            if noException:
                return False,str(e)
            else:
                raise e


    def checkResultJson(self, res: dict,noException=False):
        try:
            if self.code == 0:
                if isinstance(res, str):
                    try:
                        res = json.loads(res)
                    except Exception as e:
                        if not self.nolog:
                            self.log.error(res)
                        raise e
                elif isinstance(res, dict) or isinstance(res, list) or isinstance(res, tuple):
                    pass
                else:
                    raise Exception("结果未知类型\n"+str(res))
                if self.isJson:
                    if self._handleCheckSameType(self.json, res):
                        self._handleTypeVal("res", self.json, res)
                    else:
                        raise Exception("结果校验错误,结果和期望结果类型不一致")
                else:
                    raise Exception("结果不是json,无法比较")

            else:
                raise Exception(self.msg)
            return True,''
        except Exception as e:
            if noException:
                return False,str(e)+'\n请求具体信息：\n'+self.name+'\n'+self.reqinfo+'\n'+self.result
            else:
                print('\n请求具体信息：\n'+self.name+'\n'+self.reqinfo+'\n'+self.result)
                raise e

    def _handleCheckVal(self, name, val, checkval):
        if checkval is None:
            if val is not None:
                raise Exception(
                    str(name)+"结果校验错误,值的类型不正确,期望是null,实际是:"+str(val))
        
        if self._handleCheckType(checkval,'dict') or self._handleCheckType(checkval,'list') or self._handleCheckType(checkval,'tuple'):
            if self._handleCheckType(checkval,'list') or self._handleCheckType(checkval,'tuple'):
                if len(checkval)>0:
                    if checkval[0]=='option' or  checkval[0]=='optional':
                        return
                    if checkval[0]=='null' or checkval[0]=='none':
                        if val is None:
                            return
            raise Exception(str(name)+"结果校验错误,值的类型不正确:值为{},类型:{},期望类型{}".format(str(val), type(val), type(checkval)))
        else:
            try:
                if isinstance(checkval,optional):
                    # self.log.debug("选填："+str(name)+"  "+str(val)+"  "+str(checkval))
                    self._handleCheckVal(name,val,checkval.method)
                    return
            except Exception as e:
                self.log.warning(str(e))
                if str(e).startswith(str(name)):
                    raise e
            try:
                if isinstance(checkval,empty):
                    self.log.debug("空："+str(name)+"  "+str(val)+"  "+str(checkval))
                    if val!="":
                        raise Exception(str(name)+"结果校验错误,值的非空:"+str(val))
                    return
            except Exception as e:
                self.log.warning(str(e))
                if str(e).startswith(str(name)):
                    raise e
            try:
                if isinstance(checkval,method):
                    
                    res=checkval(val,name)
                    self.log.debug("方法："+str(name)+"  实际值："+str(val)+"  期望值："+str(checkval)+" "+"结果信息：{}，结果状态：{}，是否继续执行：{}".format(res.msg,str(res.getStatus()),str(res.IsContinue)))
                    if not res.IsContinue:
                        raise Exception(res.msg)
                    return
            except Exception as e:
                self.log.warning(str(e))
                if str(e).startswith(str(name)):
                    raise e
            self.log.debug("值："+str(name)+"  "+str(val)+"  "+str(checkval))
            if val!=checkval:
                raise Exception(str(name)+"结果校验错误,比较值不正确:{},期望是:{},期望类型是：{}".format(val, checkval,type(checkval)))
         





    def _handleCheckDict(self, name: str, val: dict, checkval: dict):

        for k, v in val.items():
            kname = name+"['{}']".format(k)
            if k in checkval:

                self._handleTypeVal(kname, v, checkval[k])
   
            else:
                checkKeyMethod = False  # 判断为key是否有动态的,记录是否有被校验过
                err = None
                for k2, v2 in checkval.items():
                    if k2 in val:
                        continue
                    if isinstance(k2,str) or isinstance(k2,int):
                        raise Exception(kname+"结果校验错误:"+str(k)+"未在期望结果中")
                    try:
                        if isinstance(k2,method):
                            try:
                                self.log.debug(kname+",key方法（{}）校验，".format(str(k2)))
                                res=k2(k,kname)
                                if res.IsContinue:
                                    try:
                                        self._handleTypeVal(kname, v, v2)
                                        checkKeyMethod = True
                                        break
                                    except Exception as e:
                                        err = e

                            except Exception as e1:
                                raise Exception(kname+"结果校验错误:方法执行报错，"+str(e1))
                    except Exception as e2:
                        raise Exception(kname+"结果校验错误:未知类型的方法执行报错，"+str(e2))


                if not checkKeyMethod:
                    if err is None:
                        raise Exception(kname+"结果校验错误:"+str(k)+"未在期望结果中")
                    else:
                        raise err
        for k, v in checkval.items():
            kname = name+"['{}']".format(k)
            if k not in val :
                try:
                    if  issubclass(k.__class__,method):
                        continue    
                except :
                    pass

                try:
                    if issubclass(v.__class__,optional):
                        self.log.debug("选填："+str(kname))
                        continue
                except:
                    pass
                raise Exception(kname+"结果校验错误:"+str(k)+"未在实际结果中")
                

                    

    def _handleCheckList(self, name: str, val: list, checkval: list):
        if len(checkval) > 0 :
            if checkval[0] == 'required':
                if len(val) == 0:
                    raise Exception(name+"结果校验错误,长度为0")
                del(checkval[0])
            if checkval[0] == 'option' or checkval[0] == 'optional' or checkval[0] == 'null' or checkval[0] == 'none':
                del(checkval[0])
            
        if len(checkval) == 1:
            index = 0
            for line in val:
                kname = name+"[{}]".format(index)
                self._handleTypeVal(kname, line, checkval[0])
                index += 1

        elif len(checkval) > 1:

            if len(val) != len(checkval):
                raise Exception(name+"结果校验错误,比较值不正确,长度不一致:" +
                                str(val)+"\n"+str(checkval))
            for lineNum in range(len(val)):
                kname = name+"[{}]".format(lineNum)
                line = val[lineNum]
                line2 = checkval[lineNum]
                if line is None:
                    if line2 is not None:
                        raise Exception(kname+"结果校验错误,比较值不正确:"+str(line))
                else:
                    if line2 is None:
                        raise Exception(kname+"结果校验错误,比较值不正确:"+str(line))

                self._handleTypeVal(kname, line, line2)

    def _handleTypeVal(self, name, val, checkval):
        if self._handleCheckType(val, 'dict'):
            if self._handleCheckSameType(val, checkval):
                self._handleCheckDict(name, val, checkval)
            else:
                raise Exception(str(
                    name)+"结果校验错误,值的类型不正确:值为{},类型:{},期望类型{}".format(str(val), type(val), type(checkval)))
        elif self._handleCheckType(val, 'list') or self._handleCheckType(val, 'tuple'):
            if self._handleCheckSameType(val, checkval):
                self._handleCheckList(name, val, checkval)
            else:
                raise Exception(str(
                    name)+"结果校验错误,值的类型不正确:值为{},类型:{},期望类型{}".format(str(val), type(val), type(checkval)))
        else:
            self._handleCheckVal(name, val, checkval)

    def _handleCheckSameType(self, val, checkval):
        return type(val) == type(checkval)

    def _handleCheckType(self, val, typename):
        for line in typename.split("|"):
            if self._handleCheckTypeOne(val, line):
                return True
        return False

    def _handleCheckTypeOne(self, val, typename):
        if typename == 'str':
            return isinstance(val, str)
        elif typename == 'dict':
            return isinstance(val, dict)
        elif typename == 'list':
            return isinstance(val, list)
        elif typename == 'tuple':
            return isinstance(val, tuple)
        elif typename == 'int':
            return isinstance(val, int)
        elif typename == 'float':
            return isinstance(val, float)
        elif typename == 'bool':
            return isinstance(val, bool)
        elif typename == 'None':
            return val is None
        else:
            raise Exception("当前不支持{}类型".format(typename))

# def xx():
#     return print
# a={
#     xx():1
# }
# print(isinstance(print,str))
# x=check.beside(1,2)
# print(issubclass(x.__class__,method))