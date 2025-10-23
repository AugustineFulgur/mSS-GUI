#公用函数
from abc import ABC,abstractmethod
import re
from settings import *
from mitmproxy.http import HTTPFlow
from enum import Enum
import gzip
from io import BytesIO
from fnmatch import fnmatch # 一般情况下，HOST用通配符匹配 有人统一一下匹配方法吗

# 最近CS写多了 但是python的OOP还是写着别扭
class RR(Enum):
    REQUEST=0
    RESPONSE=1

class CURD(Enum):
    ADD=0
    DELETE=1
    REPLACE=2

class Ctx_global(ABC):

    def __init__(self,rr=[RR.REQUEST,RR.RESPONSE]):
        self.rr=rr #[RR]
    
    def request(self, flow: HTTPFlow):
        print("GOIN")
        if not RR.REQUEST in self.rr:
            return False
        return True
    
    def response(self, flow: HTTPFlow):
        if not RR.RESPONSE in self.rr:
            return False
        return True

class Ctx_base(ABC):

    @classmethod  # 优先级 预设 > utf8 > gbk > force(自动识别)
    def autocode(cls,req,b):
        code=[]
        auto=GLOBAL.get("默认编码形式")
        content_encoding = req.headers.get("Content-Encoding", "").lower()
        if "gzip" in content_encoding:
            try:
                with gzip.GzipFile(fileobj=BytesIO(b), mode="rb") as f:
                    b = f.read()
            except gzip.BadGzipFile:
                pass
        for k,v in req.headers.items():
            try:
                if k.lower()=="content-type": auto=v.split("charset=")[1].split(";")[0].strip()
            except:
                print("CHARSET ERROR "+v)
        code.append("utf-8")
        code.append("gbk")
        for i in code:
            try:
                return b.decode(i)
            except:
                pass
        print("ERROR? 解码失败")
        return b.decode(auto,errors="ignore")

    def __init__(self,rr=[RR.REQUEST,RR.RESPONSE]):
        self.rr=rr #[RR]

    def request(self, flow: HTTPFlow):
        if flow.request.url.endswith(".mss"):
            return False # 排除自身请求
        if not RR.REQUEST in self.rr:
            return False
        if GLOBAL.get("全局范围")!=None: #判断domain是否在范围内
            for i in GLOBAL["全局范围"]:
                if i[0]=="!":
                    return not fnmatch(flow.request.host,i[1:])
                else:
                    return fnmatch(flow.request.host,GLOBAL.get("全局范围"))
        return True
    
    def response(self, flow: HTTPFlow):
        if flow.request.url.endswith(".mss"):
            return False # 排除自身请求
        if not RR.RESPONSE in self.rr:
            return False
        if GLOBAL.get("全局范围")!=None: #判断domain是否在范围内
            for i in GLOBAL.get("全局范围"):
                if i[0]=="!":
                    return not fnmatch(flow.request.host,i[1:])
                else:
                    return fnmatch(flow.request.host,GLOBAL.get("全局范围"))
        return True

class Ctx_hit_base(Ctx_base,ABC): 
    
    def __init__(self,regex,rr):
        self.regex=regex #匹配表达式
        super().__init__(rr)

    def request(self, flow: HTTPFlow):
        if not super().request(flow): return
        if flow.request.content:
                matches = re.findall(self.regex, flow.request.text)
                for match in matches:
                    flow.request.text = flow.request.text.replace(match, self.where_hit(match))

    def response(self, flow: HTTPFlow):
        if not super().response(flow): return
        if flow.response.content:
                matches = re.findall(self.regex, flow.response.text)
                for match in matches:
                    flow.response.text = flow.response.text.replace(match, self.where_hit(match))

    @abstractmethod
    def where_hit(self,string):
        pass