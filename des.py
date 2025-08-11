import re
import base64
from Crypto.Cipher import AES
from Crypto.Cipher import DES
from Crypto.Util.Padding import pad
from Crypto.Util.Padding import unpad
from mitmproxy.http import HTTPFlow
from mitmproxy.tools import main
import urllib
import binascii
from etc.base import *

# mitmdump -s mitm.py -p 8009 

class Ctx_des:

    def request(self, flow: HTTPFlow):
        # 检查请求体是否存在
        if flow.request.content:
            # 尝试解码请求体
            # 对请求体进行正则匹配,找到所有 {.*} 格式的内容
                pattern = r'entityJson=(.*)'
                matches = re.findall(pattern, flow.request.text)
                for match in matches:
                    flow.request.text = flow.request.text.replace(match, "wmf-em-personal"+urllib.parse.quote(base64.b64encode(match.encode('utf-8')).decode("ascii")))
                    print(flow.request.text)

    def response(self, flow: HTTPFlow):
        '''if flow.response.status_code == 200:
            aaa=decrypt_and_decode(flow.response.text)
            print(aaa)
            flow.response.text = aaa
          # 获取响应对象'''
        pass
    def where_hit(string):
        pass

addons = [
    Ctx_des()
]


# 定义密钥和初始向量
key = '1234567890adbcde'.encode('utf-8')
iv = 'iamdespk'.encode('utf-8')

def encrypt_and_encode(plaintext):
    # 使用 AES-128-ECB 模式加密
    cipher = AES.new(key, AES.MODE_ECB)
    plaintext = pad(plaintext.encode('utf-8'), AES.block_size)
    ciphertext = cipher.encrypt(plaintext)
    # 进行 Base64 编码
    return base64.b64encode(ciphertext).decode('utf-8')

def decrypt_and_decode(ciphertext_base64):
    # 先将Base64编码的密文解码为字节
    ciphertext_bytes = base64.b64decode(ciphertext_base64)
    
    # 创建解密器（与加密时使用相同的密钥和模式）
    cipher = AES.new(key, AES.MODE_ECB)
    
    # 解密并去除填充
    decrypted_bytes = cipher.decrypt(ciphertext_bytes)
    unpadded_bytes = unpad(decrypted_bytes, AES.block_size)
    
    # 转换为字符串
    return unpadded_bytes.decode('utf-8')


def encrypt_and_encode_DES(plaintext):
    # 使用 DES-CBC 模式加密  
    cipher = DES.new(key, DES.MODE_CBC, iv)  
    # 对明文进行填充  
    padded_plaintext = pad(plaintext.encode('utf-8'), DES.block_size)  
    # 加密  
    ciphertext = cipher.encrypt(padded_plaintext)  
    # 将加密后的二进制数据转换为 16 进制 ASCII 字符串  
    hex_ciphertext = binascii.hexlify(ciphertext).decode('utf-8')  
    return hex_ciphertext 


