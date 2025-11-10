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
from mi.mi_gui import Ctx_gui


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

# 去除guard
class Ctx_antiguard(Ctx_base):

    class __ast(AST):

        def visit_CallExpression(
            self, node
        ):  # 遍历方式充满了一种幽默感，评价是不如traverse
            if isinstance(node.callee,StaticMemberExpression) and len(node.arguments)>0 and isinstance(node.arguments[0],ArrowFunctionExpression) and len(node.arguments[0].params)==3:
                if node.callee.property.name in ["beforeEach","afterEach","beforeResolve"]:
                    Ctx_gui.logger(f"清除hook，类型{node.callee.property.name}")
                    node.callee.property.name="expireGuard"
                    node.arguments[0].body.body = [esprima.parseScript("console.log('已清除guard！')")]
            result=yield Visited(node.__dict__)
            yield result #不支持写一起 也很幽默

        def visit_Property(self, node): #谁想得到是这个函数 离谱
            if (isinstance(node.value,FunctionExpression) and len(node.value.params)==3):
                # 这个写法好省电 感动了
                if node.key.name in ["beforeEnter","beforeRouteEnter","beforeRouteUpdate","beforeRouteLeave"]:
                    Ctx_gui.logger(f"清除hook，类型{node.key.name}")
                    node.key.name="expireGuard"
                    node.value.body.body = [esprima.parseScript("console.log('已清除guard！')")]
            result=yield Visited(node.__dict__)
            yield result #不支持写一起 也很幽默
    
    def __init__(self):
        super().__init__([RR.RESPONSE])

    def response(self, flow):
        if not super().response(flow):
            return
        content = Ctx_base.autocode(flow.response, flow.response.raw_content)
        if flow.request.url.endswith(".js"): 
            flow.response.set_content(
                Ctx_antiguard.__ast(content).jsafter.encode("utf8")
            )


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
        if flow.request.url.endswith(".js"):  # 这种特征其实还不是很明晰 先就这么写 有问题直接私聊我 这缩进真sb
            if (
                len(re.findall(r"[\/][\*]{2,}[\/]", content)) > 5
                and "/*! exports provided: default */" in content
            ):
                flow.response.set_content(
                    Ctx_packeaziler.__ast(content).jsafter.encode("utf8")
                )
