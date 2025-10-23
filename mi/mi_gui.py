# GUI类，默认地址为/[TOKEN]-console.mss
from etc.base import *
from settings import *
import os
import datetime
from mitmproxy import http
from jinja2 import Template
import json


# 这个理论上也是单例，但是这语言写单例麻烦死了
class Ctx_gui(Ctx_global):

    addons=[]
    log=""

    def logger(s):
        print(s)
        Ctx_gui.log+=datetime.datetime.now().strftime("[%Y-%m-%d %H:%M:%S] ")+s+"\n"

    @classmethod    
    def get_addons_head(cls):
        re={}
        for i in cls.addons:
            for k,v in i.addons_head().items():
                re[k]=v
        return re

    @classmethod
    def get_addons_log(cls):
        # 只更新增量数据，前端使用IndexedDB存储
        re={}
        for i in cls.addons:
            for k,v in i.addons_log().items():
                re[k]=v
            i.addons_log_clean()
        return re

    def __init__(self):
        self.log=[] # 日志
        super().__init__([RR.REQUEST])
        self.token= os.urandom(6).hex() if TOKEN=="" else TOKEN #不是同一个时间但是同一个三目这一块
        print("当前token为："+self.token)

    def request(self,flow):
        # 控制台去掉token设置，不过token还有用
        if (flow.request.headers.get("Host") if flow.request.headers.get("Host") else flow.request.host) not in ["mss.local"]: return # console的路径为mss.local/console.mss
        if flow.request.path.endswith("console.mss"): # console就不添加了
            with open("console.html","r",encoding="utf-8") as c: # 
                flow.response=http.Response.make(200,Template(c.read()).render(g=GLOBAL.all(),addons_head=Ctx_gui.get_addons_head()).encode("utf-8"),{"Content-Type": "text/html; charset=utf-8"})
        if flow.request.path.endswith("log.mss"):
            flow.response=http.Response.make(200,Ctx_gui.log.encode("utf-8"),headers={"Content-Type": "text/plain; charset=utf-8"})
            Ctx_gui.log="" # 清空log
        if flow.request.path.endswith("addons.mss"):
            flow.response=http.Response.make(200,json.dumps(Ctx_gui.get_addons_log()).encode("utf-8"),headers={"Content-Type": "text/plain; charset=utf-8"})
        if flow.request.path.endswith("api.mss"): # 这边请求会根据glob更新GLOBAL
            glob=flow.request.json()
            try:
                with lock:
                    for i in glob:
                        GLOBAL.set(i,glob[i])
            except Exception as e:
                Ctx_gui.logger(e)
            flow.response=http.Response.make(200,"OK")
            
class GUI(ABC): # 合并两个类，没有必要的事情就少做了
    def __init__(self,name:str,head:list):
        self.head=head
        self.log=[]
        self.name=name
        Ctx_gui.addons.append(self)

    # 没有getset居然有点烦
    def addons_log(self):
        return {self.name:self.log}
    
    def addons_log_clean(self):
        self.log=[]

    def addons_head(self):
        print(self.name)
        return {self.name:self.head}
    
    
