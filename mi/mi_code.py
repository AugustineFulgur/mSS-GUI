import base64
import binascii
from etc.base import *
from enum import Enum

class CODE(Enum):
    BASE64=0
    HEX=1

class FT(Enum):
    FROM=0
    TO=1

class Ctx_code(Ctx_hit_base):

    def __init__(self, regex, rr,code,ft,encode='utf-8'):
        self.encode=encode
        self.code=code #ENCODE
        self.ft=ft #FT
        super().__init__(regex, rr)

    def where_hit(self, string):
        if FT==FT.FROM:
            return Ctx_code.decode(string,self.code,self.encode)
        else:
            return Ctx_code.encode(string,self.code,self.encode)
        
    def decode(string: str, tocode, encode):
        if tocode == CODE.BASE64:
            return base64.b64decode(string.encode(encode))
        elif tocode == CODE.HEX:
            return binascii.unhexlify(string.encode(encode))

    def encode(string:str, tocode,encode):
        if tocode == CODE.BASE64:
            return base64.b64encode(string.encode(encode))
        elif tocode == CODE.HEX:
            return binascii.hexlify(string.encode(encode))
    
    def encode(binary: bytes, tocode):
        if tocode == CODE.BASE64:
            return base64.b64encode(binary)
        elif tocode == CODE.HEX:
            return binascii.hexlify(binary)