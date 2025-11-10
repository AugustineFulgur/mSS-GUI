from __future__ import unicode_literals
from esprima.visitor import Visitor, Visited
from esprima.nodes import *
import esprima
import etc.__escodegen as escodegen
from abc import ABC,abstractmethod

# 这Visitor的逻辑不是人看的 ^ ^
class AST(Visitor,ABC):

    def __init__(self,js:str):
        super().__init__()
        self.js=js
        self.code=None
        self.code=esprima.parseScript(self.js)
        self.jsafter=escodegen.generate(self.visit(self.code))