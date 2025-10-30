from __future__ import unicode_literals
from esprima.visitor import Visitor, Visited
from esprima.nodes import *
import esprima
import escodegen
from abc import ABC,abstractmethod

# 这Visitor的逻辑不是人看的 ^ ^
class AST(Visitor,ABC):

    def __init__(self,js:str):
        super().__init__()
        self.js=js
        self.code=None
        try:
            self.code=esprima.parseScript(self.js)
        except:
            pass
        finally:
            self.code=esprima.parseModule(self.js)
        self.jsafter=escodegen.generate(self.visit(self.code))



if __name__ == "__main__":
    

    with open("1.js","r",encoding="utf8") as f:
        js_code=f.read()

    extractor = AST(js_code)
    with open("2.js","w",encoding="utf8") as f:
        f.write(escodegen.generate(extractor.jsafter))