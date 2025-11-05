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
    def autocode(cls,req,b:bytes) -> str: # 谁给我缩进。
        code=[]
        auto=GLOBAL.get("默认编码形式")
        if "gzip" in req.headers.get("Content-Encoding", "").lower():
            try:
                with gzip.GzipFile(fileobj=BytesIO(b), mode="rb") as f:
                    b = f.read()
            except gzip.BadGzipFile:
                pass
            try:
                auto=req.headers.get("Content-Encoding", "").split("charset=")[1].split(";")[0].strip()
            except:
                print("CHARSET ERROR ")
        code.append("utf-8")
        code.append("gbk")
        for i in code:
            try:
                return b.decode(i)
            except:
                pass
        print("ERROR? 解码失败")
        return b.decode(auto,errors="ignore")
    
    @classmethod
    def raw_request(cls,request) -> bytes:
        return f"{request.method} {request.path} {request.http_version or 'HTTP/1.1'}\r\n".encode("utf-8") \
            + request.headers.__bytes__() \
            + b"\r\n" \
            + request.raw_content
    
    @classmethod
    def raw_response(cls,response) -> bytes:
        # 额外处理下GZIP
        content=response.raw_content
        if "gzip" in response.headers.get("Content-Encoding", "").lower():
            try:
                with gzip.GzipFile(fileobj=BytesIO(response.raw_content), mode="rb") as f:
                    content = f.read()
            except gzip.BadGzipFile:
                pass
        return f"{response.http_version or 'HTTP/1.1'} {str(response.status_code)} {response.reason or ''}\r\n".encode("utf-8") \
            + response.headers.__bytes__() \
            + b"\r\n" \
            + content


    def __init__(self,rr=[RR.REQUEST,RR.RESPONSE]):
        self.rr=rr #[RR]

    def request(self, flow: HTTPFlow):
        if flow.request.url.endswith(".mss"):
            return False # 排除自身请求
        if not RR.REQUEST in self.rr:
            return False
        if GLOBAL.get("全局范围")!="": #判断domain是否在范围内
            for i in GLOBAL["全局范围"]:
                if i[0]=="!":
                    return not fnmatch((flow.request.headers.get("Host") if flow.request.headers.get("Host") else flow.request.host),i[1:])
                else:
                    return fnmatch((flow.request.headers.get("Host") if flow.request.headers.get("Host") else flow.request.host),GLOBAL.get("全局范围"))
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