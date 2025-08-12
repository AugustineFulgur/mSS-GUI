from etc.base import *

class Ctx_head(Ctx_base):

    def __init__(self, rr,head:dict,curd):
        super().__init__(rr)
        self.head=head
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