from etc.base import *
from mi.mi_crypt import *
from mi.mi_head import *
from mi.mi_encode import *

addons = [
    Ctx_encrypt("a=([0-9]*)",[RR.REQUEST],ALGO.AES,AES.MODE_CBC,'1234567887654321'.encode('utf-8'),CODE.BASE64,'utf-8','1234567887654321'.encode('utf-8')),
    #Ctx_code("a=([0-9]*)",[RR.REQUEST],CODE.BASE64)
]
