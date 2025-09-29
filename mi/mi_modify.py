# head和body的处理和替换
from etc.base import *

class Ctx_head(Ctx_base):

    def __init__(self, rr,s1:str,curd,s2:str=""):
        super().__init__(rr)
        self.head={s1:s2}
        self.curd=curd #CURD
    
    def request(self, flow: HTTPFlow):
        if not super().request(flow): return
        self.do_curd(flow.request)
        

    def response(self, flow: HTTPFlow):
        if not super().response(flow): return
        self.do_curd(flow.response)

    def do_curd(self,req):
        for i in self.head:
            if self.curd==CURD.ADD:
                req.headers[i.key]=i.value
            elif self.curd==CURD.DELETE:
                del req.headers[i.key]
            elif self.curd==CURD.REPLACE:
                # 从一些角度上必要但另一些角度上不必要的东西
                req.headers[i.key]=i.value
            elif self.curd==CURD.LOOKUP:
                # CAUTION
                # 请在这里修改以适配
                print(req.headers[i.key])

class Ctx_content(Ctx_base):

    def __init__(self, rr,s1:str,curd,s2:str=""):
        super().__init__(rr)
        self.s=s1
        self.s2=s2
        self.curd=curd #CURD
    
    def request(self, flow: HTTPFlow):
        if not super().request(flow): return
        self.do_curd(flow.request)   

    def response(self, flow: HTTPFlow):
        if not super().response(flow): return
        self.do_curd(flow.response)

    def do_curd(self,req):
        for i in self.head:
            if self.curd==CURD.DELETE:
                req.content.replace(self.s,"")
            elif self.curd==CURD.REPLACE:
                # 从一些角度上必要但另一些角度上不必要的东西
                req.content.replace(self.s,self.s2)

class Ctx_all(Ctx_base):
    
    def __init__(self, rr,s:str,curd,s2:str=None):
        super().__init__(rr)
        self.s=s
        self.s2=s2
        self.curd=curd #CURD
        self.head=Ctx_head(rr,s,curd,s2)
        self.content=Ctx_content(rr,s,curd,s2)

    def request(self, flow):
        if not super().request(flow): return
        self.head.request(flow)
        self.content.request(flow)
    
    def response(self, flow):
        if not super().response(flow): return
        self.head.response(flow)
        self.content.response(flow)