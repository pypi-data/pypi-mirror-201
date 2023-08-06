
import logging


gData={}

log = logging.getLogger('')

def setGlobal(key,val,path=''):
    gData[key]=val
    log.debug('添加{}的值为公共参数：{} = {}'.format(path,key,val))

def getGlobal(key,default=""):
    val=""
    if key in gData:
        val= gData[key]
    else:
        val= default
    log.debug('返回公共参数：{} = {}'.format(key,val))
    return val

