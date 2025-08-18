#公用函数
from abc import ABC,abstractmethod
import re
import run
from mitmproxy.http import HTTPFlow
from enum import Enum
from fnmatch import fnmatch # 一般情况下，HOST用通配符匹配 有人统一一下匹配方法吗

# 最近CS写多了 但是python的OOP还是写着别扭
class RR(Enum):
    REQUEST=0
    RESPONSE=1

class CURD(Enum):
    ADD=0
    DELETE=1
    REPLACE=2
    LOOKUP=3

class Ctx_global(ABC):

    def __init__(self,rr=[RR.REQUEST,RR.RESPONSE]):
        self.rr=rr #[RR]

class Ctx_base(ABC):

    def __init__(self,rr=[RR.REQUEST,RR.RESPONSE]):
        self.rr=rr #[RR]

    def request(self, flow: HTTPFlow):
        if not RR.REQUEST in self.rr:
            return False
        if run.GLOBAL_DOMAIN!=None: #判断domain是否在范围内
            for i in run.GLOBAL_DOMAIN:
                if i[0]=="!":
                    return not fnmatch(flow.request.host,i[1:])
                else:
                    return fnmatch(flow.request.host,run.GLOBAL_DOMAIN)
        return True
    
    def response(self, flow: HTTPFlow):
        if not RR.RESPONSE in self.rr:
            return False
        if run.GLOBAL_DOMAIN!=None: #判断domain是否在范围内
            for i in run.GLOBAL_DOMAIN:
                if i[0]=="!":
                    return not fnmatch(flow.request.host,i[1:])
                else:
                    return fnmatch(flow.request.host,run.GLOBAL_DOMAIN)
        return True

class Ctx_hit_base(Ctx_base,ABC): 
    
    def __init__(self,regex,rr):
        self.regex=regex #匹配表达式
        super().__init__(rr)

    def request(self, flow: HTTPFlow):
        if not super().request(flow): return
        if flow.request.content:
                matches = re.findall(self.regex, flow.request.text)
                print(matches)
                for match in matches:
                    print(match)
                    print(self.where_hit(match))
                    flow.request.text = flow.request.text.replace(match, self.where_hit(match))
                # DEBUG
                print(flow.request.text)

    def response(self, flow: HTTPFlow):
        if not super().response(flow): return
        if flow.response.content:
                matches = re.findall(self.regex, flow.response.text)
                for match in matches:
                    flow.response.text = flow.response.text.replace(match, self.where_hit(match))
                # DEBUG
                print(flow.response.text)

    @abstractmethod
    def where_hit(self,string):
        pass