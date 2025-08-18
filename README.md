MITM常见脚本合集。

## 0 为什么使用mitmproxy（mitmdump）
1. 安装方便，使用`pip install mitmproxy`即可
2. 可移植性高，一次加解密可以在各种工具（bp、sqlmap、以及其他支持代理的利用工具）上使用，达到无感加解密。如工具本身不支持使用代理，考虑使用proxifier。
3. BP插件写着太烦人了^ ^

## 1 使用方式
首先在run.py中添加要加载的函数（类）并设置参数。
然后在terminal中启动mitmdump。其中，mitm可以以以下两种形式启动（还有更多方式，请见mitmproxy的文档）：
①只监听，可用于各种流量工具的自动加解密如burpsuite、sqlmap tamper，或自定义包格式等。
`mitmdump -s [mitm.py] -p [port]` 
②做中转代理，如sqlmap->mitm->burpsuite
`mitmdump -s [mitm.py] -p [in-port] --mode upstream:http://localhost:[out-port]`

## 2 脚本介绍

### 2.0 基类

#### Ctx_global
- rr[list,enum] 可取值RR.REQUEST（请求）和RR.RESPONSE（响应），表示当前模块是否对请求、响应生效，如[RR.REQUEST,RR.RESPONSE]。
不受全局变量影响，对所有请求/响应包生效。

#### Ctx_base
- rr[list,enum] 可取值RR.REQUEST（请求）和RR.RESPONSE（响应），表示当前模块是否对请求、响应生效，如[RR.REQUEST,RR.RESPONSE]。

#### Ctx_hit_base < Ctx_base
- regex[str] 捕获表达式，这个类**仅捕获请求体和响应体**。需要注意的是对请求体`a=1`，表达式`a=[0-9]*`捕获`a=1`，表达式`a=([0-9]*)`捕获1。

### 2.1 加解密

#### mi_crypt.Ctx_encrypt/Ctx_decrypt < Ctx_hit_base
包括Ctx_encrypt（加密）和Ctx_decrypt（解密），目前支持的算法为AES/DES/RSA/SM4。使用前请记得安装依赖。
**可以与burpsuite联动以实现无感请求包解密。**
- algo[enum] 可取值为ALGO.DES/ALGO.AES/ALGO.RSA/ALGO.SM4...表示加解密使用的算法。
- mode[Crypt] 加密模式，如AES.CBC。
- key[byte] 密钥，如'1234567887654321'.encode('utf-8')
- output[enum] 可取值为CODE.BASE64/CODE.HEX，加密的输出格式或解密的输入格式。
- encoding[str] 编码格式，默认值为utf-8。
- iv[str|byte] 一般情况下为偏移量，格式参考key。在RSA解密模式，为私钥的password，str格式。
``` python
Ctx_encrypt(
    "a=([0-9]*)",
    [RR.REQUEST],
    ALGO.AES,
    AES.MODE_CBC,
    '1234567887654321'.encode('utf-8'),
    CODE.BASE64,
    'utf-8',
    '1234567887654321'.encode('utf-8')
)

Ctx_encrypt(regex,rr,algo,mode,key,[output,encoding,iv])
```
#### mi_code.Ctx_code < Ctx_hit_base
目前支持base64和hex的编码解码。
- ft[enum] 可取值为FT.FROM/FT.TO，分别对应解码/编码。
- code[enum] 可取值为CODE.BASE64/CODE.HEX，指示编码格式。
``` python
Ctx_code(
    "a=([0-9]*)",
    [RR.REQUEST],
    FT.FROM,
    CODE.BASE64
)

Ctx_code(regex,rr,ft,code)
```

### 2.2 头处理

#### mi_head.Ctx_head < Ctx_base
可以对请求和响应中的head进行增、删、改、打印（这里可以通过修改源码扩展内容）。
- head[dict] 字典，需要进行修改的头和值，当操作为删除时value可以随意取值。
- curd[enum] 可取值为CURD.ADD/CURD.DELETE/DURD.REPLACE/CURD.LOOKUP，指示对应增删改查操作。
``` python
Ctx_head(
    [RR.REQUEST],
    {{"Authorization","Bearer 55yL5ZWl5ZGiXiBe"}},
    CURD.ADD
)

Ctx_head(rr,head,curd)
```

### 2.3 流量优化

#### mi_notrace.Ctx_drop_wechat301 < Ctx_base
自动drop请求微信登录的包。一般在“用浏览器打开微信公众号链接”时用到。
无参。
``` python
Ctx_drop_wechat301(
)

Ctx_drop_wechat301(rr=[RR.REQUEST])
```

#### mi_notrace.Ctx_ua < Ctx_base
修改请求使用的User-Agent。目前有手机、爬虫、微信小程序三个UA。
- ua[UA] 可取值为UA.PHONE/UA.SPIDER/UA.WXMINIPROGRAM
``` python
Ctx_ua(
    UA.PHONE
)

Ctx_head(ua)
```

## 3 全局变量

可以在run.py中设置以下全局变量以控制脚本的全局行为：
- GLOBAL_DOMAIN[list] 列表，指定脚本生效的domain范围。由于普遍习惯，使用**通配符**而非正则进行匹配。毕竟在正则的情况下*.4399.com就需要写成.*\.4399\.com，感觉稍微有点反人类了。
    - 正向匹配，可以使用如：*.4399.com
    - **如需要反向排除，请在单词最前部分使用感叹号（!）**，如：!\*.4399.com

## -1 更新日志

`一些不必要的更新是在凑COMMIT。`
这个项目会持续更新，如有需求可以向我的github邮箱发送邮件。
由于项目在施工中，每次commit可能会存在部分未完成的代码。使用脚本请参考文档。
- 0.0.1 开天辟地，拥有基础功能
- 0.0.2 修复BUG
- 0.0.3 完善文档部分
- 0.0.4 修改文档排版，新增SM4加解密，添加全局变量和头处理
- 0.0.5 增加一些用于流量优化的脚本