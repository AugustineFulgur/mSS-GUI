# webpack应用专用的脚本，扒js之类的

from etc.base import *
import re
import time
import requests

class Ctx_forcejs(Ctx_base):

    def __init__(self):
        super().__init__([RR.RESPONSE])

    def response(self, flow):
        if not super().response(flow): return
        if re.search(r"(app|main|index)\.[a-zA-Z0-9]{1,}\.js",flow.request.url):
            # 随便写写
            rss=re.findall("[\"'](chunk-[a-zA-Z0-9]{1,})[\"']\:\s?[\"']([a-zA-Z0-9]{1,})[\"']",flow.response.text)
            res=flow.response.text
            for c,k in rss:
                print(c,k)
                jsurl="{0}/{1}.{2}.js".format(flow.request.url.rsplit('/', 1)[0],c,k)
                if requests.head(jsurl).status_code!=200: continue #跳过不是js文件的部分
                res+="document.head.appendChild(document.createElement('script')).src ='{0}';".format(jsurl)
            flow.response.text=res

class Ctx_cors(Ctx_base):
    pass # 对CORS包的优化，减少渗透中出现前端代码写得屎JS未加载出来的情况，比如自动给https网站使用httpsjs，删除CORS跨域响应头。


class Ctx_url(Ctx_base):
    
    def __init__(self):
        super().__init__([RR.RESPONSE])