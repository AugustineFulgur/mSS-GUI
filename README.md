MITM常见脚本合集。

## 0 为什么使用mitmproxy（mitmdump）
1. 安装方便，使用`pip install mitmproxy`即可
2. 可移植性高，一次加解密可以在各种工具（bp、sqlmap、以及其他支持代理的利用工具）上使用。如工具本身不支持使用代理，考虑使用proxifier。
3. BP插件写着太烦人了^ ^

## 1 使用方式
首先在run.py中添加要加载的函数（类）并写好参数。
然后在terminal中启动mitmdump。其中，mitm可以以以下两种形式启动（还有更多方式，请见mitmproxy的文档）：
①只监听，可用于各种流量工具的自动加解密如burpsuite、sqlmap tamper，或自定义包格式等。
`mitmdump -s [mitm.py] -p [port]` 
②做中转代理，如sqlmap->mitm->burpsuite
`mitmdump -s [mitm.py] -p [in-port] --mode upstream:http://localhost:[out-port]`

## 2 脚本介绍

### 2.0 基类

##### Ctx_base
- rr[list,enum] 可取值RR.REQUEST（请求）和RR.RESPONSE（响应），表示当前模块是否对请求、响应生效，如\[RR.REQUEST,RR.RESPONSE\]。

##### Ctx_hit_base < Ctx_base
- regex[str] 捕获表达式，这个类**仅捕获请求体和响应体**。需要注意的是对请求体`a=1`，表达式`a=[0-9]*`捕获`a=1`，表达式`a=([0-9]*)`捕获1。

### 2.1 加解密

#### mi_crypt < Ctx_hit_base
包括Ctx_encrypt（加密）和Ctx_decrypt（解密）。
目前支持的算法为AES/DES/RSA。
- algo[enum] 可取值为ALGO.DES/ALGO.AES/ALGO.RSA...表示加解密使用的算法。
- mode[Crypt] 加密模式，如AES.CBC。
- key[byte] 密钥，如'1234567887654321'.encode('utf-8')
- output[enum] 可取值为CODE.BASE64/CODE.HEX，加密的输出格式或解密的输入格式。
- encoding[str] 编码格式，默认值为utf-8。
- iv[str|byte] 一般情况下为偏移量，格式参考key。在RSA解密模式，为私钥的password，str格式。