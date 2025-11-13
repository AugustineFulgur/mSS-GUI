from __future__ import unicode_literals
from esprima.visitor import Visitor, Visited
from esprima.nodes import *
import esprima
import etc.__escodegen as escodegen
from abc import ABC
from collections import deque
import types

# 这Visitor的逻辑不是人看的 ^ ^
class AST(Visitor,ABC):

    def __init__(self,js:str):
        super().__init__()
        self.js=js
        self.code=esprima.parseScript(self.js)
        self.jsafter=escodegen.generate(self.visit(self.code))


    def webpack_var1knot(self,knot,varname):
        # 在某一模块（knot）寻找某一变量的定义 比如节5502中变量e为n('1234')
        pass
