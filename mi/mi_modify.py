# head和body的处理和替换
from etc.base import *
from mi.mi_gui import *
import re


class Ctx_head(Ctx_base):

    def __init__(self, rr, s1: str, curd, s2: str = ""):
        super().__init__(rr)
        self.head = {s1: s2}
        self.curd = curd  # CURD

    def request(self, flow: HTTPFlow):
        if not super().request(flow):
            return
        self.do_curd(flow.request)

    def response(self, flow: HTTPFlow):
        if not super().response(flow):
            return
        self.do_curd(flow.response)

    def do_curd(self, req):
        if self.curd == CURD.ADD:
            req.headers[self.s1] = self.s2
        elif self.curd == CURD.DELETE:
            del req.headers[self.s1]
        elif self.curd == CURD.REPLACE:
            # 从一些角度上必要但另一些角度上不必要的东西
            req.headers[self.s1] = self.s2
        elif self.curd == CURD.LOOKUP:
            # CAUTION
            # 请在这里修改以适配
            Ctx_gui.logger("捕获HEADER"+req.headers[self.s1])


class Ctx_content(Ctx_base):

    def __init__(self, rr, s1: str, s2: str = ""):
        super().__init__(rr)
        self.s = s1
        self.s2 = s2

    def request(self, flow: HTTPFlow):
        if not super().request(flow):
            return
        self.do_curd(flow.request)

    def response(self, flow: HTTPFlow):
        if not super().response(flow):
            return
        self.do_curd(flow.response)

    def do_curd(self, req):
        req.text = Ctx_base.autocode(req, req.raw_content)


class Ctx_all(Ctx_base):

    def __init__(self, rr, s: str, s2: str = None):
        super().__init__(rr)
        self.s = s
        self.s2 = s2
        self.head = Ctx_head(rr, s, CURD.REPLACE, s2)
        self.content = Ctx_content(rr, s, s2)

    def request(self, flow):
        if not super().request(flow):
            return
        self.head.request(flow)
        self.content.request(flow)

    def response(self, flow):
        if not super().response(flow):
            return
        self.head.response(flow)
        self.content.response(flow)


class Ctx_rlookup(Ctx_base, GUI):

    def __init__(self, rr, reg: list, showname="RLOOKUP"):
        Ctx_base.__init__(self, rr)
        GUI.__init__(self, showname, ["关键词", "结果"])
        self.reg = reg

    def request(self, flow):
        if not super().request(flow):
            return
        request = Ctx_base.autocode(
            flow.request, Ctx_base.raw_request(flow.request))
        for r in self.reg:
            for i in re.findall(r, request, re.DOTALL):
                self.log.append([r, i])
                Ctx_gui.logger("命中："+i)

    def response(self, flow):
        if not super().response(flow):
            return
        response = Ctx_base.autocode(
            flow.response, Ctx_base.raw_response(flow.response))
        for r in self.reg:
            for i in re.findall(r, response, re.DOTALL):
                self.log.append([r, i])
                Ctx_gui.logger("命中："+i)
