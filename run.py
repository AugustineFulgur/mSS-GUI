from etc.base import *
from mi.mi_crypt import *
from mi.mi_modify import *
from mi.mi_code import *
from mi.mi_notrace import *
from mi.mi_webpack import *
from mi.mi_gui import *
from mi.mi_monkey import *
from enum import Enum

addons = [
    #Ctx_rlookup([RR.RESPONSE],[r"[\"'](/[a-zA-Z0-9_\?=]{2,})[\"']"],"路由提取"),
    #Ctx_gui(), #请保证GUI在其它继承GUI类的插件调用后被调用
    #Ctx_forcejs(),
    #Ctx_packeaziler(),
    #Ctx_monkey([("hello.js",MONKEYSCRIPT.INNERTAIL)])
]
