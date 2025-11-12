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

    def visit(self, obj): # 它这个visitor吧 遍历到BlockStatement的时候直接传给visitor_list去了 虽然理解方式 但是这样给我得工作带来了非常 大 的 麻烦 
        # 重写了visit 让它在遍历到body:BlockStatement的时候停下 这样可以在迫不得已的时候使用这个函数处理
        """Visit a Object."""
        if not hasattr(self, 'visitors'):
            self._visit_context = {}
            self._visit_count = 0
        try:
            self._visit_count += 1
            stack = deque()
            stack.append((obj, None))
            last_result = None
            while stack:
                try:
                    last, visited = stack[-1]
                    if isinstance(last, types.GeneratorType):
                        stack.append((last.send(last_result), None))
                        last_result = None
                    elif isinstance(last, Visited):
                        stack.pop()
                        last_result = last.result
                    elif isinstance(last, Object):
                        if(last.body and isinstance(last.body,BlockStatement)):
                            visitor = getattr(self, 'visit_BlockStatement', self.visit_Object)
                        elif last in self._visit_context:
                            if self._visit_context[last] == self.visit_Object:
                                visitor = self.visit_RecursionError
                            else:
                                visitor = self.visit_Object
                        else:
                            method = 'visit_' + last.__class__.__name__
                            visitor = getattr(self, method, self.visit_Object)
                        self._visit_context[last] = visitor
                        stack.pop()
                        stack.append((visitor(last), last))
                    else:
                        method = 'visit_' + last.__class__.__name__
                        visitor = getattr(self, method, self.visit_Generic)
                        stack.pop()
                        stack.append((visitor(last), None))
                except StopIteration:
                    stack.pop()
                    if visited and visited in self._visit_context:
                        del self._visit_context[visited]
            return last_result
        finally:
            self._visit_count -= 1
            if self._visit_count <= 0:
                self._visit_context = {}


    def webpack_var1knot(self,knot,varname):
        # 在某一模块（knot）寻找某一变量的定义 比如节5502中变量e为n('1234')
        pass

    def visit_BlockStatement(self,node):
        # 这里偷点懒 应该没事 有事再改
        for i in node.body if type(node.body)==list else node.body.body:
            yield i
        yield Visited(node)