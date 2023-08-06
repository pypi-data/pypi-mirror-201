import queue


import threading
import time

import os
import functools



class myThread (threading.Thread):
    def __init__(self, func):
        '''
        自定义线程
        func 执行的方法
        '''
        threading.Thread.__init__(self)
        self.func = func

    def run(self):
        name = threading.currentThread().name
        # 获得线程的名称,传入方法
        self.func(name)



class handleMuprocess:
    def __init__(self, num,writeRecord=False):
        ''''
        用于使用线程,并发
        num,并发数
        '''
        self.num = num #并发数量
        self.q = queue.Queue() #输入的队列
        self.func = None
        self.initFunc = None#配置初始化方法,一个线程运行一次
        self.endFunc=None
        self.runlist = []  # 线程的list
        self.qout=queue.Queue() #输出的队列
        self.freeSet=set()
        self.tmpDict={}#存临时数据
        self.wr=writeRecord
        self.wrf=None
        self.finalf=None
        self.firstf=None

        self.writeRecord()

    def put(self, value,addout=False):
        '''
        输入队列的存入
        '''
        if value is not None:
            if addout:
                self.qout.put(value)
            else:
                self.q.put(value)
        else:
            print('[warn]当前put不支持存放None值')

    def get(self,isOut=False):
        '''
        输入队列的获得值,没有值获得None
        '''
        try:
            if isOut:
                return self.qout.get(timeout=1)
            else:
                return self.q.get(timeout=1)
        except:
            return None


    def start(self):
        '''
        开始运行线程
        '''
        #添加结束线程
        if self.endFunc is not None:
            self.runlist.append(myThread(self.endFunc))
        #过滤没有方法的情况
        if self.func is None:
            raise Exception('没有运行的方法,请检查~')
        #配置线程
        for _ in range(self.num):
            self.runlist.append(myThread(self.func))
        # 配置进度文件
        if self.wr:
            self.runlist.append(myThread(self.wrf))
        if self.firstf is not None:
            self.firstf()
        #运行
        for t in self.runlist:
            t.start()
        
        for t in self.runlist:
            t.join()
        if self.finalf is not None:
            self.finalf()
        

    def setRunFunc(self, func):
        '''
        添加方法,仅运行逻辑,不需要考虑巡皇
        如果有返回值需要处理,setOutFunc(func(name,value,tdict))来使用,返回格式是bool,obj/[obj];返回None，不处理
        当bool为true,放在结果处理,false返回队列
        func要求参数,1/name,2/获得的值,3/临时dict
        当获得值为None时,停止
        '''
        @functools.wraps(func)
        def f(name):
            try:
                if self.initFunc is not None:
                    self.initFunc(name,False)
                while True:
                    value = self.get()
                    if value is not None:
                        if name in self.freeSet:
                            self.freeSet.remove(name)
                        res=func(name, value,self.tmpDict)
                        if res is not None:
                            if res[0]:
                                self.put(res[1],True)
                            else:
                                if isinstance(res[1],list) or isinstance(res[1],tuple):
                                    for val in res[1]:
                                        self.put(val)
                                else:
                                    self.put(res[1])
                    else:
                        # print(name,len(self.freeSet))
                        
                        self.freeSet.add(name)
                        if len(self.freeSet)==self.num:
                            # print(name,'end')
                            break
                        else:
                            time.sleep(10)
                            continue
                # print(name, '运行结束')
                if self.initFunc is not None:
                    self.initFunc(name,True)
            except Exception as e:
                # print(e)
                self.put(str(e)+'\n',True)

                self.freeSet.add(name)
        self.func = f
    
    def setOutFunc(self,func):
        '''
        添加方法,仅运行逻辑,不需要考虑
        func要求参数,1/name,2/获得的值,3/临时dict,
        当获得值为None时,停止
        '''
        @functools.wraps(func)
        def f(name):
            try:
                while True:
                    value = self.get(True)
                    if value is not None:
                        res=func(name,value,self.tmpDict)
                        if res is not None:
                            if res[0]:
                                pass
                                
                                # self.put(res[1],True)
                            else:
                                if isinstance(res[1],list) or isinstance(res[1],tuple):
                                    for val in res[1]:
                                        self.put(val,True)
                                else:
                                    self.put(res[1],True)
                    else:
                        if len(self.freeSet)==self.num:
                            break
                        else:
                            time.sleep(2)
                            continue
            except Exception as e:
                print('[warn]结束方法出现问题:'+str(e))
        self.endFunc = f

    def setInitFunc(self,func): 
        @functools.wraps(func)
        def f(name,isEnd):
            func(name,self.tmpDict,isEnd)
        self.initFunc = f
    def setFinalFunc(self,func): 
        @functools.wraps(func)
        def f():
            func(self.tmpDict)
        self.finalf = f
    def setFirstFunc(self,func): 
        @functools.wraps(func)
        def f():
            func(self.tmpDict)
        self.firstf = f
    
    def writeRecord(self,*l,**k):
        def f(*l,**k):
            if os.path.exists('handleRecord.txt'):
                os.remove('handleRecord.txt')
            while True:
                time.sleep(5)
                
                if len(self.freeSet)==self.num:
                    break
                else:
                    ss=str(time.strftime('%Y%m%d %H:%M:%S' , time.localtime()))+"->"
                    ss+="总线程数:{},当前运行线程数:{},队列剩余数量:{}\n".format(str(self.num),str(self.num-len(self.freeSet)),str(self.q.qsize()))
                    with open("handleRecord.txt",'a',encoding='utf8') as f:
                        f.write(ss)
        self.wrf=f




#样例
def demo(n, v,d):
    # time.sleep(random.randint(1, 20)/100)
    if str(v) not in d and int(v) > 3:
        return False,v       

    
    d[str(v)]=True
    
    print(n,v,d)
    return True,v

#样例2
def demo2(n,v,d):
    # time.sleep(random.randint(1, 2))
    print('emd',n,v,d)

#样例3
def demo3(n,d,isEnd):
    # time.sleep(random.randint(1, 2))
    print(n,d,isEnd)

# t = handleMuprocess(3)

# for i in range(20):
#     t.put(i)

# t.setRunFunc(demo)


# t.start()

# ---------------------------------------

# first(tmpdict:dict)

# for{
#     init(name,tmpDict,isEnd=False)
#     Runfunc(name, value,tmpDict)  True-> OutFunc(name, value,tmpDict)
#     init(name,tmpDict,isEnd=True)
# }


# final(tmpdict:dict)

