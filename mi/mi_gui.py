# GUI类，默认地址为/[TOKEN]-console.mss
from etc.base import *
from settings import *
import os
from mitmproxy import http
from jinja2 import Template

c=open("console.html","r",encoding="utf-8").read()

# 这个理论上也是单例，但是这语言写单例麻烦死了
class Ctx_gui(Ctx_global):

    addons=[]

    def log(s):
        print(s)
        with open("mss.log","a+",encoding="utf-8") as f:
            f.write(s+"\n") 

    @classmethod    
    def get_addons_head(cls):
        re={}
        for i in cls.addons:
            for k,v in i.addons_head().items():
                re[k]=v
        return re

    @classmethod
    def get_addons_log(cls):
        # 这里应该可以节约下，但是都本地网络了好像也没必要，除非有非常多数据？
        re={}
        for i in cls.addons:
            for k,v in i.addons_log().items():
                re[k]=v
            i.addons_log_clean()
        return re

    def __init__(self):
        with open("mss.log","w+",encoding="utf-8") as f:
            f.write("") # 清空log
        super().__init__([RR.REQUEST])
        self.token= os.urandom(6).hex() if TOKEN=="" else TOKEN #不是同一个时间但是同一个三目这一块
        print("当前token为："+self.token)

    def request(self,flow):
        if flow.request.path.endswith("console.mss"): # console就不添加了
            Ctx_gui.log(str(Ctx_gui.addons))
            print(Ctx_gui.addons)
            flow.response=http.Response.make(200,Template(c).render(g=GLOBAL.all(),addons_head=Ctx_gui.get_addons_head()).encode("utf-8"),{"Content-Type": "text/html; charset=utf-8"})
        if flow.request.path.endswith(self.token+"-log.mss"):
            with open("mss.log","r",encoding="utf-8") as f:
                flow.response=http.Response.make(200,f.read().encode("utf-8"))
        if flow.request.path.endswith(self.token+"-addons.mss"):
            flow.response=http.Response.make(200,str(Ctx_gui.get_addons_log()).encode("utf-8"))
        if flow.request.path.endswith(self.token+"-api.mss"): # 这边请求会根据glob更新GLOBAL
            glob=flow.request.json()
            try:
                with lock:
                    for i in glob:
                        GLOBAL.set(i,glob[i])
            except Exception as e:
                Ctx_gui.log(e)
            flow.response=http.Response.make(200,"OK")
            print(GLOBAL.all())
            
class GUI_addons():
    def __init__(self,name:str,head:list):
        self.head=head
        self.log=[]
        self.name=name

    # 没有getset居然有点烦
    def addons_log(self):
        return {self.name:self.log}
    
    def addons_log_clean(self):
        self.log=[]

    def addons_head(self):
        print(self.name)
        return {self.name:self.head}
    

class Ctx_addon(ABC): # 有点莞莞类卿了

    def __init__(self,name,head):
        self.addon=GUI_addons(name,head)
        Ctx_gui.addons.append(self.addon)
    
