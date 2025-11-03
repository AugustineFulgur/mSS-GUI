# webpack应用专用的脚本，扒js之类的

from etc.base import *
import re
import time
import requests
from mitmproxy import http
from etc.jsast import AST
import esprima
from esprima.visitor import Visited
from esprima.nodes import *


class Ctx_forcejs(Ctx_base):

    def __init__(self):
        super().__init__([RR.RESPONSE])

    def response(self, flow):
        if not super().response(flow):
            return
        if re.search(r"(app|main|index)\.[a-zA-Z0-9]{1,}\.js", flow.request.url):
            # 随便写写
            rss = re.findall(
                "[\"'](chunk-[a-zA-Z0-9]{1,})[\"']\:\s?[\"']([a-zA-Z0-9]{1,})[\"']",
                Ctx_base.autocode(flow.response, flow.response.raw_content),
            )
            res = flow.response.text
            for c, k in rss:
                jsurl = "{0}/{1}.{2}.js".format(
                    flow.request.url.rsplit("/", 1)[0], c, k
                )
                if requests.head(jsurl).status_code != 200:
                    continue  # 跳过不是js文件的部分
                res += "document.head.appendChild(document.createElement('script')).src ='{0}';".format(
                    jsurl
                )
            flow.response.text = res


# 根据js响应提取API
class Ctx_url(Ctx_base):

    def __init__(self):
        super().__init__([RR.RESPONSE])


# 优化未开启作用域提升情况下的代码
class Ctx_packeaziler(Ctx_base):

    class __ast(AST):

        def visit_FunctionExpression(
            self, node
        ):  # 遍历方式充满了一种幽默感，评价是不如traverse
            if (node.id is None) and (len(node.params) == 3):
                for i in range(len(node.body.body)):
                    if (
                        isinstance(
                            node.body.body[i].expression, CallExpression)
                        and isinstance(node.body.body[i].expression.callee, Identifier)
                        and node.body.body[i].expression.callee.name == "eval"
                    ):
                        node.body.body[i] = esprima.parseScript(
                            node.body.body[i].expression.arguments[0].value
                        )
            result = yield node.__dict__
            yield Visited(result)

    def __init__(self):
        super().__init__([RR.RESPONSE])

    def response(self, flow):
        # 其实应该用re写 考虑到后续的扩展性还是使用ast
        if not super().response(flow):
            return
        content = Ctx_base.autocode(flow.response, flow.response.raw_content)
        if re.search(
            r"(app|main|index).*\.js", flow.request.url
        ):  # 这种特征其实还不是很明晰 先就这么写 有问题直接私聊我
            if (
                len(re.findall(r"[\/][\*]{2,}[\/]", content)) > 5
                and "/*! exports provided: default */" in content
            ):
                flow.response.set_content(
                    Ctx_packeaziler.__ast(content).jsafter.encode("utf8")
                )
