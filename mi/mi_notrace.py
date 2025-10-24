# 自动Drop、自动删除用户信息、禁止跳转到微信客户端、自动手机UA、自动禁止蜜罐信息收集（也就是drop所有qq、知乎、微博、贴吧的包，考虑仅在渗透时开启）
from etc.base import *
from enum import Enum
import re

#Drop微信跳转包
class Ctx_drop_wechat301(Ctx_global):

    def request(self, flow):
        if not super().request(flow): return
        if flow.request.host=="open.weixin.qq.com" and "connect/oauth2/authorize" in flow.request.url:
            flow.kill()

    def response(self, flow: HTTPFlow):
        if not super().request(flow): return
        if flow.response.status_code==301 and "open.weixin.qq.com" in flow.response.headers["Location"]:
            flow.kill()

class UA(Enum):
    #UA的枚举 枚举可以是字符串太好了
    PHONE="Mozilla/5.0 (Linux; Android 13; CPH2389) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Mobile Safari/537.36 OppoBrowser/13.1.0.1"
    SPIDER="Mozilla/5.0 (compatible; Bingbot/2.0; +http://www.bing.com/bingbot.htm)"
    WXMINIPROGRAM="Mozilla/5.0 (Linux; Android 13; MI 13) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36 MicroMessenger/8.0.40 MiniProgram/3.0.0"

class Ctx_ua(Ctx_global):

    def __init__(self, ua:UA):
        super().__init__([RR.REQUEST])
        self.ua=ua

    def request(self, flow):
        if not super().request(flow): return
        flow.request.headers["User-Agent"]=self.ua.value

class Ctx_drop(Ctx_global):

    def __init__(self, hint:list):
        super().__init__([RR.REQUEST])
        self.hint=hint

    def request(self, flow):
        url=flow.request.url
        for i in self.hint:
            if re.search(i, url):
                flow.kill()
# 自动禁止蜜罐信息收集（也就是drop所有qq、知乎、微博、贴吧的包，考虑仅在渗透时开启） 使用Ctx_drop的特定配置。 这个施工中