# 使用AST功能需要额外导入esprima 我会补充到requirements里
from visitor import *
from abc import ABC,abstractmethod
import esprima
import escodegen
from mi.mi_gui import Ctx_gui



class AST(ABC): # 生活不如意，就写pythonOOP

    # 匹配函数
    @abstractmethod
    def expr(self,node:Node) -> bool:
        pass

    # 执行函数 要扩展输入的时候重载或者多写个成员变量就行
    @abstractmethod
    def do(self,node:Node) -> None:
        pass

    def bake(self,js:str,url:str="") -> None:
        try:
            program = objectify(esprima.parseScript(js).toDict())
            for node in program.traverse():
                if self.expr(node): self.do(node)
            print(escodegen.generate(program))

        except:
            pass
            Ctx_gui.logger(f"AST发生错误，位置:{url or '未知'}")

