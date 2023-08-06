

import datetime
import json
import logging
import re
import time
from .gl import setGlobal,getGlobal

log = logging.getLogger('')

null=None
true=True
false=False

class Result(object):
    def __init__(self, status=4, msg='') -> None:
        self.__status = status
        self.msg = msg
        # self.st = status

    def __transform(self):
        if self.__status == 0:
            return 'ignore'
        elif self.__status == 1:
            return "ok"
        elif self.__status == 2:
            return "skip"
        elif self.__status == 3:
            return 'failed'
        else:
            return 'error'

    def __str__(self) -> str:
        if len(self.msg.strip()) > 0:
            return self.__transform()+","+self.msg
        else:
            return self.__transform()

    def getStatus(self) -> str:
        return self.__transform()

    @property
    def IsIgnore(self):
        return self.__status == 0

    @property
    def IsOK(self):
        return self.__status == 1

    @property
    def IsSKIP(self):
        return self.__status == 2

    @property
    def IsContinue(self):
        return self.__status < 3

    @staticmethod
    def ignore(message: str):

        return Result(0, message)

    @staticmethod
    def ok(message: str = ""):

        return Result(1, message)

    @staticmethod
    def skip(message: str):
        return Result(2, message)

    @staticmethod
    def failed(message: str):
        return Result(3, message)

    @staticmethod
    def error(message: str):
        return Result(4, message)


class method:
    '''
    def __init(self) 这里是输入参数的地方
    def run(self,realVal, valPath) -> Result.xxx
    '''

    def __call__(self, realVal, valPath) -> Result:
        try:
            self.realVal = realVal
            self.valPath = valPath
            run = self.__getattribute__('run')
            return run(realVal, valPath)
        except Exception as e:
            return Result.error(self.__class__.__name__+"实现run方法错误："+str(e))

    def __str__(self) -> str:
        try:
            return self.__class__.__name__ + ",收到值：{}，值的路径：{}".format(self.realVal, self.valPath)
        except:
            return self.__class__.__name__+" "


class _within(method):
    def __init__(self, val) -> None:
        self.val = val

    def run(self, realVal, valPath):
        if len(self.val) > 0:
            for v in self.val:
                if str(v) == str(realVal):
                    return Result.ok("")
            return Result.failed(valPath+":实际结果({})不在期望[{}]之中".format(realVal, ','.join(self.val)))
        else:
            return Result.error(valPath+":未维护within方法的值")


class _without(method):
    def __init__(self, val) -> None:
        self.val = val

    def run(self, realVal, valPath):
        if len(self.val) > 0:
            for v in self.val:
                if str(v) == str(realVal):
                    return Result.failed(valPath+":实际结果({})在期望[{}]之中".format(realVal, ','.join(self.val)))
            return Result.ok('')
        else:
            return Result.error(valPath+":未维护within方法的值")


class _between(method):
    def __init__(self, val1, val2) -> None:
        self.res = None
        try:
            val1 = float(val1)
            val2 = float(val2)
        except:
            self.res = ':维护错误,between方法需要两个数字类型的值'
        if self.res is None:
            if val2 > val1:
                self.sval = val1
                self.bval = val2
            else:
                self.sval = val2
                self.bval = val1

    def run(self, realVal, valPath):
        if self.res is None:
            rval = 0
            try:
                rval = float(realVal)
            except:
                return Result.failed(valPath+":实际结果({}),非数字类型".format(realVal))
            if rval >= self.sval and rval <= self.bval:
                return Result.ok()
            else:
                return Result.failed(valPath+":实际结果({})不在期望[{},{}]之内".format(realVal, self.sval, self.bval))
        else:
            return Result.error(valPath+self.res)


class _beside(method):
    def __init__(self, val1, val2) -> None:
        self.res = None
        try:
            val1 = float(val1)
            val2 = float(val2)
        except:
            self.res = ':维护错误,beside方法需要两个数字类型的值'
        if self.res is None:
            if val2 > val1:
                self.sval = val1
                self.bval = val2
            else:
                self.sval = val2
                self.bval = val1

    def run(self, realVal, valPath):
        if self.res is None:
            rval = 0
            try:
                rval = float(realVal)
            except:
                return Result.failed(valPath+":实际结果({}),非数字类型".format(realVal))
            if rval >= self.sval and rval <= self.bval:
                return Result.failed(valPath+":实际结果({})不在期望[{},{}]之外".format(realVal, self.sval, self.bval))

            else:
                return Result.ok()

        else:
            return Result.error(valPath+self.res)


class _startWith(method):
    def __init__(self, val) -> None:
        super().__init__()
        self.val = str(val)

    def run(self, realVal, valPath):
        if str(realVal).startswith(self.val):
            return Result.ok()
        else:
            return Result.failed(valPath+":实际结果({})不在期望({})开头".format(realVal, self.val))


class _noStartWith(method):
    def __init__(self, val) -> None:
        super().__init__()
        self.val = str(val)

    def run(self, realVal, valPath):
        if str(realVal).startswith(self.val):
            return Result.failed(valPath+":实际结果({})不期望({})开头".format(realVal, self.val))
        else:
            return Result.ok()


class _endWith(method):
    def __init__(self, val) -> None:
        super().__init__()
        self.val = str(val)

    def run(self, realVal, valPath):
        if str(realVal).endswith(self.val):
            return Result.ok()
        else:
            return Result.failed(valPath+":实际结果({})不在期望({})开头".format(realVal, self.val))


class _notEndWith(method):
    def __init__(self, val) -> None:
        super().__init__()
        self.val = str(val)

    def run(self, realVal, valPath):
        if str(realVal).endswith(self.val):
            return Result.failed(valPath+":实际结果({})不期望({})开头".format(realVal, self.val))
        else:
            return Result.ok()


class _contain(method):
    def __init__(self, val) -> None:
        super().__init__()
        self.val = val

    def run(self, realVal, valPath):
        if len(self.val) > 0:
            for v in self.val:
                if str(v) in str(realVal):
                    return Result.ok("")
            return Result.failed(valPath+":实际结果({})不在包含期望[{}]之中".format(realVal, ','.join(self.val)))
        else:
            return Result.error(valPath+":未维护contain方法的值")


class _notContain(method):
    def __init__(self, val) -> None:
        super().__init__()
        self.val = val

    def run(self, realVal, valPath):
        if len(self.val) > 0:
            for v in self.val:
                if str(v) in str(realVal):

                    return Result.failed(valPath+":实际结果({})不包含期望[{}]之中".format(realVal, ','.join(self.val)))
            return Result.ok("")
        else:
            return Result.error(valPath+":未维护notContain方法的值")


def _handleCheckTypeOne(val, typename, oldString=False):
    if typename == 'str':
        return isinstance(val, str)
    elif typename == 'dict':
        if oldString:
            try:
                if isinstance(val, str):
                    val = json.loads(val)
            except:
                pass

        return isinstance(val, dict)
    elif typename == 'list':
        if oldString:
            try:
                if isinstance(val, str):
                    val = json.loads(val)
            except:
                pass
        return isinstance(val, list)
    elif typename == 'tuple':
        return isinstance(val, tuple)
    elif typename == 'int':
        if oldString:
            try:
                if isinstance(val, str):
                    val = int(val)
            except:
                pass
        return isinstance(val, int)
    elif typename == 'float':
        if oldString:
            try:
                if isinstance(val, str):
                    val = float(val)
            except:
                pass
        return isinstance(val, float)
    elif typename == 'bool':
        if oldString:
            try:
                if isinstance(val, str):
                    if val.upper() == "TRUE" or val.upper() == "FALSE":
                        return True
                else:
                    return False
            except:
                pass

        return isinstance(val, bool)
    elif typename == 'None':
        return val is None
    else:
        raise Exception("当前不支持{}类型".format(typename))


class empty(object):

    def __str__(self) -> str:
        return "校验空方法"
    pass


class optional(object):

    def __init__(self, method) -> None:
        self.method = method

    def __str__(self) -> str:
        try:
            return "校验选填方法:"+str(self.method)
        except:
            return "校验选填方法"


class _notEmpty(method):
    def __init__(self) -> None:
        super().__init__()

    def run(self, realVal, valPath):
        if len(realVal) > 0:
            return Result.ok("")
        else:
            return Result.failed(valPath+":实际结果：长度为空,期望不为空")


class _notEmptyString(method):
    def __init__(self) -> None:
        super().__init__()

    def run(self, realVal, valPath):
        if isinstance(realVal, str) and len(realVal) > 0:
            return Result.ok("")
        else:
            if isinstance(realVal, str):
                return Result.failed(valPath+":实际结果：长度为空,期望不为空")
            else:
                return Result.failed(valPath+":实际结果类型{}不是字符串".format(type(realVal)))


class _checkType(method):
    def __init__(self, val: str, old: bool) -> None:
        super().__init__()
        self.val = val
        self.old = old

    def run(self, realVal, valPath):
        try:
            if _handleCheckTypeOne(realVal, self.val, self.old):
                return Result.ok()
            else:
                return Result.failed(valPath+":实际结果类型({}),期望类型是'{}'".format(type(realVal), self.val))
        except Exception as e:
            return Result.error(valPath+":实际结果类型({}),期望类型报错".format(type(realVal), str(e)))

class _time(method):
    def __init__(self,format) -> None:
        super().__init__()
        self.format=format
    def run(self, realVal, valPath):
        try:
            if isinstance(realVal,str):
                t=int(time.mktime(time.strptime(realVal,self.format)))
                if t>0 and t<1995700751:
                    return Result.ok()
                else:
                    return Result.error(valPath+":时间比较出错,实际结果：{}，期望类型：{}".format(realVal,self.format))   
            else:
                return Result.error(valPath+":时间比较出错,实际结果：{},类型：{}，期望类型：字符串".format(realVal,type(realVal)))

        except Exception as e:
            return Result.error(valPath+":时间比较出错,实际结果：{}，期望类型：{}，报错：{}".format(realVal,self.format, str(e)))




class _any(method):
    def __init__(self) -> None:
        super().__init__()

    def run(self, realVal, valPath):
        return Result.ok()
# class _checkStringType(method):
#     def __init__(self,val:str) -> None:
#         super().__init__()
#         self.val = val

#     def run(self, realVal, valPath):
#         try:
#             if _handleCheckTypeOne(realVal,self.val):
#                 return Result.ok()
#             else:
#                 return Result.failed(valPath+":实际结果类型({}),期望类型是'{}'".format(type(realVal),self.val))
#         except Exception as e :
#             return Result.error(valPath+":实际结果类型({}),期望类型报错".format(type(realVal),str(e)))


class _regular(method):
    def __init__(self, reg) -> None:
        super().__init__()
        self.reg = reg

    def run(self, realVal, valPath):
        try:
            res = re.fullmatch(self.reg, str(realVal))
            if res is None:
                return Result.failed(valPath+":正则匹配错误，请检查正则表达：{}，实际结果：{}".format(str(self.reg), str(realVal)))
            else:
                return Result.ok(str(res))
        except Exception as e:
            return Result.error(valPath+":正则匹配失败，请检查正则表达：{}，实际结果：{}，错误：{}".format(str(self.reg), str(realVal), str(e)))

class _save(method):
    def __init__(self, key) -> None:
        super().__init__()
        self.key = key
    
    def run(self, realVal, valPath):
        try:
            setGlobal(self.key,realVal,valPath)
            return  Result.ok()
        except Exception as e:
            return Result.error(valPath+":获取值错误，key：{}，实际结果：{}，错误：{}".format(str(self.key), str(realVal), str(e)))
        

class checkOwnType:
    def __init__(self, old=False) -> None:
        self.old = old

    @property
    def STR(self):
        return _checkType('str', self.old)

    @property
    def DICT(self):
        return _checkType('dict', self.old)

    @property
    def LIST(self):
        return _checkType('list', self.old)

    @property
    def TUPLE(self):
        return _checkType('tuple', self.old)

    @property
    def FLOAT(self):
        return _checkType('float', self.old)

    @property
    def BOOL(self):
        return _checkType('bool', self.old)

    @property
    def INT(self):
        return _checkType('int', self.old)

    @property
    def NULL(self):
        return _checkType('None', self.old)

    def regular(self, format):
        '''
        \d  匹配所有的十进制数字  0-9
        \D  匹配所有的非数字，包含下划线
        \s  匹配所有空白字符（空格、TAB等）
        \S  匹配所有非空白字符，包含下划线
        \w  匹配所有字母、汉字、数字    a-z A-Z 0-9
        \W  匹配所有非字母、汉字、数字，包含下划线
   --------------------------
    1、$：匹配一行的结尾（必须放在正则表达式最后面）
    2、^：匹配一行的开头（必须放在正则表达式最前面）
    3、*：前面的字符可以出现0次或多次（0~无限）
    4、+：前面的字符可以出现1次或多次（1~无限）
    5、?：变"贪婪模式"为"勉强模式"，前面的字符可以出现0次或1次
    6、.：匹配除了换行符"\n"之外的任意单个字符
    7、|：两项都进行匹配
    8、[ ]：代表一个集合，有如下三种情况
    [abc]：能匹配其中的单个字符
    [a-z0-9]：能匹配指定范围的字符，可取反（在最前面加入^）
    [2-9] [1-3]：能够做组合匹配
    9、{ }：用于标记前面的字符出现的频率，有如下情况：

    {n，m}：代表前面字符最少出现n次，最多出现m次
    {n，}：代表前面字符最少出现n次，最多不受限制
    {，m}：代表前面字符最多出现n次，最少不受限制
    {n}：前面的字符必须出现n次
        '''
        return _regular(format)


class _than(method):
    def __init__(self, val: int or float, type: str) -> None:
        super().__init__()
        self.val = val
        self.type = type

    def run(self, realVal, valPath):
        try:
            res = False
            if self.type == '>':
                if realVal > self.val:
                    res = True
            elif self.type == '>=':
                if realVal >= self.val:
                    res = True
            elif self.type == '<':
                if realVal < self.val:
                    res = True
            elif self.type == '<=':
                if realVal <= self.val:
                    res = True
            elif self.type == '<>' or self.type == '!=':
                if realVal != self.val:
                    res = True
            if res:
                return Result.ok(valPath+':比较大小，'+str(realVal)+self.type+str(self.val))
            else:
                return Result.failed(valPath+":比较大小错误，实际结果：{}".format(str(realVal)+self.type+str(self.val)))

        except Exception as e:
            return Result.error(valPath+":比较大小错误，实际结果：实际结果：{}，错误：{}".format(str(realVal)+self.type+str(self.val), str(e)))


class _OR(method):
    def __init__(self, cond) -> None:
        super().__init__()
        self.cond = cond

    def __str__(self) -> str:
        if len(self.cond) > 0:
            sdc = ""
            for x in self.cond:
                sdc += ","+str(x)
            return super().__str__()+",其中方法是："+sdc
        else:
            return super().__str__()

    def run(self, realVal, valPath):
        err = str(valPath)+","
        if len(self.cond) == 0:
            return Result.error(str(valPath)+",未配置校验方法，请检查~")
        for m in self.cond:
            try:
                if issubclass(m.__class__, empty):
                    if realVal == "":
                        return Result.ok()
                    else:
                        err += "结果比较错误，结果非空："+str(realVal)
                        continue
            except Exception as e:
                pass
            try:
                if issubclass(m.__class__, method):
                    try:
                        res = m(realVal, valPath)
                        
                        if res.IsContinue:
                            return Result.ok()
                        else:
                            err += res.msg+"  "
                            continue
                    except Exception as e:
                        err += str(m)+":"+str(e)+"  "
            except:
                pass
            # if realVal == m:
            #     return Result.ok()
            # else:
            #     err += "比较错误，结果不相等：'{}'  与  '{}'".format(realVal, m)

        return Result.failed(str(err))


class _AND(method):
    def __init__(self, cond) -> None:
        super().__init__()
        self.cond = cond

    def __str__(self) -> str:
        if len(self.cond) > 0:
            sdc = ""
            for x in self.cond:
                sdc += ","+str(x)
            return super().__str__()+",其中方法是："+sdc
        else:
            return super().__str__()

    def run(self, realVal, valPath):

        if len(self.cond) == 0:
            return Result.error(str(valPath)+",未配置校验方法，请检查~")
        for m in self.cond:
            try:
                if issubclass(m.__class__, empty):
                    if realVal == "":
                        continue
                    else:
                        return Result.failed("结果比较错误，结果非空："+str(realVal))

            except Exception as e:
                pass
            try:
                if issubclass(m.__class__, method):
                    try:
                        res = m(realVal, valPath)
                        if res.IsContinue:
                            continue
                        else:
                            return res

                    except Exception as e:
                        return Result.error(str(m)+":"+str(e))
            except:
                pass
            # if realVal == m:
            #     continue
            # else:
            #     return Result.failed("比较错误，结果不相等：'{}'  与  '{}'".format(realVal, m))

        return Result.ok()

class _url(method):
    def __init__(self) -> None:
        super().__init__()

    def run(self, realVal, valPath):
        if re.match(r'^https?:/{2}\w.+$', str(realVal)):
            return Result.ok()
        else:
            return Result.error(str(valPath)+",非url格式，请检查："+str(realVal))

class _hap(method):
    def __init__(self) -> None:
        super().__init__()

    def run(self, realVal, valPath):
        if re.match(r'^hap:/{2}\w.+$', str(realVal)):
            return Result.ok()
        else:
            return Result.error(str(valPath)+",非hap格式，请检查："+str(realVal))


class check(object):
    def __init__(self) -> None:
        pass

    @staticmethod
    def OR(*condition):
        return _OR(condition)

    @staticmethod
    def NULL(*condition):
        c = list(condition)
        c.insert(0, check.checkType().NULL)
        return _OR(c)

    @staticmethod
    def AND(*condition):
        return _AND(condition)

    @staticmethod
    def empty(*condition):
        '''
        结果值允许为空
        '''
        c = list(condition)
        c.insert(0, empty())
        return _OR(c)

    @staticmethod
    def emptyAndString():
        return check.empty(check.checkType().STR)

    @staticmethod
    def url():
        return _url()

    @staticmethod
    def hap():
        return _hap()

    @staticmethod
    def timeFormat(format="%Y-%m-%d %H:%M:%S"):
        '''
        %y 两位数的年份表示（00-99）

%Y 四位数的年份表示（000-9999）

%m 月份（01-12）

%d 月内中的一天（0-31）

%H 24小时制小时数（0-23）

%I 12小时制小时数（01-12） 

%M 分钟数（00=59）

%S 秒（00-59）
%f 毫秒（0-999999）

%a 本地简化星期名称

%A 本地完整星期名称

%b 本地简化的月份名称

%B 本地完整的月份名称

%c 本地相应的日期表示和时间表示

%j 年内的一天（001-366）

%p 本地A.M.或P.M.的等价符

%U 一年中的星期数（00-53）星期天为星期的开始

%w 星期（0-6），星期天为星期的开始

%W 一年中的星期数（00-53）星期一为星期的开始

%x 本地相应的日期表示

%X 本地相应的时间表示

%Z 当前时区的名称

%% %号本身 
        '''
        return _time(format)



    @staticmethod
    def save(key,*condition):
        '''
        保存值
        '''
        c=_save(key)
        if len(condition)>0:
            return check.AND(c,_OR(condition))
        else:
            return c

    # @staticmethod
    # @property
    # def STRING():
    #     return "str"

    # @staticmethod
    # @property
    # def INT():
    #     return "int"

    # @staticmethod
    # @property
    # def FLOAT():
    #     return "float"

    # @staticmethod
    # @property
    # def BOOL():
    #     return "bool"

    # @staticmethod
    # @property
    # def NULL():
    #     return "None"

    @staticmethod
    def within(*val):
        '''
        判断值是否在指定内
        样例:within('yes','no')
        '''
        return _within([str(x) for x in val])

    @staticmethod
    def without(*val):
        '''
        判断值是否在指定外
        样例:without('one','two')
        '''
        return _without([str(x) for x in val])

    @staticmethod
    def between(val1: int, val2: int):
        '''
        判断数值是否在指定的范围内
        样例:between(1,200)
        '''
        return _between(val1, val2)

    @staticmethod
    def beside(val1: int, val2: int):
        '''
        判断数值是否在指定的范围外
        样例:beside(1,200)
        '''
        return _beside(val1, val2)

    @staticmethod
    def startWith(val):
        '''
        判断值是否以指定开头
        样例:startWith('xxx')
        '''
        return _startWith(val)

    @staticmethod
    def notStartWith(val):
        '''
        判断值是否不以指定开头
        样例:notStartWith('xxx')
        '''
        return _noStartWith(val)

    @staticmethod
    def endWith(val):
        '''
        判断值是否以指定结尾
        样例:endWith('xxx')
        '''
        return _endWith(val)

    @staticmethod
    def notEndtWith(val):
        '''
        判断值是否不以指定结尾
        样例:notEndtWith('xxx')
        '''
        return _notEndWith(val)

    @staticmethod
    def notEmpty():
        '''
        结果值不空就对了
        '''
        return _notEmpty()

    @staticmethod
    def notEmptyString():
        '''
        结果值是字符串且不空就对了
        '''
        return _notEmptyString()

    @staticmethod
    def optional(value):
        '''
        结果值允许不存在,传入校验值
        '''
        return optional(value)

    @staticmethod
    def contain(*val):
        '''
        结果值包含一些值
        '''
        return _contain([str(x) for x in val])

    @staticmethod
    def notContain(*val):
        '''
        结果值包含一些值
        '''
        return _notContain([str(x) for x in val])

    @staticmethod
    def checkType(t: str = ""):
        '''
        结果值的类型
        '''
        if t != "":
            return _checkType(t)
        else:
            return checkOwnType()

    @staticmethod
    def checkStringType(t: str = ""):
        '''
        结果值字符串的类型
        '''
        if t != "":
            return _checkType(t, True)
        else:
            return checkOwnType(True)

    @staticmethod
    def any():
        '''
        任意结果值
        '''
        return _any()

    def greaterThan(val):
        '''
        大于
        '''
        return _than(val, '>')

    def greaterEqThan(val):
        '''
        大于等于
        '''
        return _than(val, '>=')

    def lessThan(val):
        '''
        小于
        '''
        return _than(val, '<')

    def lessEqThan(val):
        '''
        小于等于
        '''
        return _than(val, '<=')

    def noteq(val):
        '''
        不等于
        '''
        return _than(val, '!=')


def test():
    # v=check.within()('1223','asdas/das/da/s')
    v = check.between(123, '1.5')('5', 'xxx')
    print(v)
    v = check.beside(123, 222)('155', 'xxx')

    print(v)


class demoClass(method):
    def __init__(self) -> None:
        super().__init__()

    def run(self, v1, v2):
        if v1 == v2:
            return Result.ok()
        else:
            return Result.failed('xxxx')


# test()
# print(demoClass()(1,1))
# a=check.optional("")
# print(isinstance(a,optional))
# print(a.__class__,optional,issubclass(a.__class__,optional))
# __save(1)