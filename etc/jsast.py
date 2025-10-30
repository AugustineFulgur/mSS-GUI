from __future__ import unicode_literals
from esprima.visitor import Visitor, Visited
from esprima.nodes import *
import esprima
import escodegen

# 这Visitor的逻辑不是人看的 ^ ^
class AST(Visitor):

    def __init__(self,js:str):
        super().__init__()
        self.js=js
        self.in_target_func = False
        self.code=None
        try:
            self.code=esprima.parseScript(self.js)
        except:
            pass
        finally:
            self.code=esprima.parseModule(self.js)
        self.jsafter=self.visit(self.code)

    def visit_FunctionExpression(self, node):
        prev_state = self.in_target_func
        self.in_target_func = (node.id is None) and (len(node.params) == 3)
        result = yield node.__dict__  
        self.in_target_func = prev_state
        yield Visited(result)  

    def visit_CallExpression(self, node):
        if self.in_target_func:
            if (isinstance(node.callee, Identifier) and node.callee.name == "eval" and isinstance(node.arguments[0],Literal)):
                # 改这里
                yield Visited(esprima.parseScript(node.arguments[0].value).body[0].expression)
                return # 写得我快飞升了，主要你py的yield跟其它语言的yield不是一个yield
        result = yield node.__dict__
        yield Visited(result)

if __name__ == "__main__":
    

    with open("1.js","r",encoding="utf8") as f:
        js_code=f.read()

    extractor = AST(js_code)
    with open("2.js","w",encoding="utf8") as f:
        f.write(escodegen.generate(extractor.jsafter.toDict()))