#公用函数
from abc import ABC,abstractmethod
import re
import base64
from mitmproxy.http import HTTPFlow
import urllib
from enum import Enum

#最近CS写多了 但是python的OOP还是写着别扭
class RR(Enum):
    REQUEST=0
    RESPONSE=1

class CURD(Enum):
    ADD=0
    DELETE=1
    REPLACE=2
    LOOKUP=3

class Ctx_base(ABC):

    def __init__(self,rr):
        self.rr=rr #[RR]

    def request(self, flow: HTTPFlow):
        return False if not RR.REQUEST in self.rr else True

    def response(self, flow: HTTPFlow):
        return False if not RR.RESPONSE in self.rr else True

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