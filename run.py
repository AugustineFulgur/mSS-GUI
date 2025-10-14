from etc.base import *
from mi.mi_crypt import *
from mi.mi_modify import *
from mi.mi_code import *
from mi.mi_notrace import *
from mi.mi_webpack import *
from mi.mi_gui import *
from enum import Enum

addons = [
    Ctx_rlookup([RR.RESPONSE],"ht(.*)l"),
    Ctx_gui(),
    # Ctx_forcejs(),
]
