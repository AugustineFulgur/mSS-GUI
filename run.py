from etc.base import *
from mi.mi_crypt import *
from mi.mi_head import *
from mi.mi_code import *
from mi.mi_notrace import *
from enum import Enum




addons = [
    #Ctx_encrypt("a=([0-9]*)",[RR.REQUEST],ALGO.AES,AES.MODE_CBC,'1234567887654321'.encode('utf-8'),CODE.BASE64,'utf-8','1234567887654321'.encode('utf-8')),
    Ctx_ua(UA.WXMINIPROGRAM)
]
