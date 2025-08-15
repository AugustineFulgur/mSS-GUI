from Crypto.Cipher import AES
from Crypto.Cipher import DES
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Util.Padding import pad
from Crypto.Util.Padding import unpad
from gmssl.sm4 import CryptSM4, SM4_ENCRYPT, SM4_DECRYPT
from etc.base import *
from mi.mi_code import Ctx_code

# 加解密脚本，包括AES,DES,RSA，其它加密方式请续写
# 使用方式
# 详情请看README
# Ctx_encrypt(".*",[RR.REQUEST],ALGO.AES,AES.MODE_ECB,'gbk','123456'.encoding('utf8'),AES.block_size)

class ALGO(Enum):
    AES=1
    DES=2
    RSA=3
    SM4=4

#加密
class Ctx_encrypt(Ctx_hit_base):

    def __init__(self, regex, rr,algo,mode,key,output=None,encoding='utf-8',iv=None):
        super().__init__(regex, rr)
        self.key=key
        self.iv=iv #可以不写
        self.algo=algo #ALGO
        self.mode=mode #AES.MODE_ECB,etcs
        self.encoding=encoding #编码
        self.output=output #TOCODE.BASE64 OR TOCODE.HEX
    #不自动补全我身上有克苏鲁在爬

    def where_hit(self,string):
        ciphertext=string
        if self.algo==ALGO.AES:
            cipher = AES.new(self.key, self.mode, self.iv)
            plaintext = pad(string.encode(self.encoding), AES.block_size)
            ciphertext = cipher.encrypt(plaintext)
        elif self.algo==ALGO.DES:
            cipher = DES.new(self.key, self.mode, self.iv)
            plaintext = pad(string.encode(self.encoding), DES.block_size)
            ciphertext = cipher.encrypt(plaintext)
        elif self.algo==ALGO.RSA:
            cipher_rsa = PKCS1_OAEP.new(RSA.import_key(self.key))
            plaintext_bytes = string.encode(self.encoding)
            ciphertext = cipher_rsa.encrypt(plaintext_bytes)
        elif self.algo==ALGO.SM4:
            #对国密4适配
            sm4 = CryptSM4()
            sm4.set_key(self.key, SM4_ENCRYPT)
            plaintext_bytes = string.encode(self.encoding)
            ciphertext = sm4.crypt_ecb(plaintext_bytes)
        return Ctx_code.encode(ciphertext,self.output).decode(self.encoding)
    
#解密
class Ctx_decrypt(Ctx_hit_base):

    def __init__(self, regex, rr,algo,mode,key,input=None,encoding='utf-8',ivorpass=None,block=None):
        super().__init__(regex, rr)
        self.key=key
        self.ivorpass=ivorpass #可以不写，在RSA模式为私钥的key
        self.algo=algo #ALGO
        self.mode=mode #AES.MODE_ECB,etcs
        self.block=block
        self.encoding=encoding #编码
        self.input=input #TOCODE.BASE64 OR TOCODE.HEX
    #不自动补全我身上有克苏鲁在爬

    def where_hit(self, string):
        plaintext = string
        string=Ctx_code.decode(string,self.input,self.encoding)
        if self.algo == ALGO.AES:
            cipher = AES.new(self.key, self.mode, self.iv)
            decrypted_bytes = cipher.decrypt(string)
            plaintext = unpad(decrypted_bytes, AES.block_size).decode(self.encoding)
        elif self.algo == ALGO.DES:
            cipher = DES.new(self.key, self.mode, self.iv)
            decrypted_bytes = cipher.decrypt(string)
            plaintext = unpad(decrypted_bytes, DES.block_size).decode(self.encoding)
        elif self.algo == ALGO.RSA:
            cipher_rsa = PKCS1_OAEP.new(RSA.import_key(self.key,self.ivorpass))
            decrypted_bytes = cipher_rsa.decrypt(string)
            plaintext = decrypted_bytes.decode(self.encoding)
        elif self.algo == ALGO.SM4:
            sm4 = CryptSM4()
            sm4.set_key(self.key, SM4_DECRYPT)
            decrypted_bytes = sm4.crypt_ecb(string)
            plaintext = decrypted_bytes.decode(self.encoding)
        return plaintext