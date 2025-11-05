# 类油猴脚本，在html类返回包中嵌入脚本

from etc.base import *
from mitmproxy import http
from enum import Enum
from mi.mi_gui import Ctx_gui
from mitmproxy import http
import re
from lxml import etree # 总而言之用解析效果好点

MONKEY_FOLDER = "monkey/"  # 文件统一放在根目录monkey下


class MONKEYSCRIPT(Enum):
    INNERHEAD = 0  # html标签后
    INNERTAIL = 1  # /html标签前
    OUTSIDE = 2  # 额外文件，/html标签前


class Ctx_monkey(Ctx_base):

    # 写得越来越专业了 欣赏ing 话又说回来 py在泛类型上越走越窄 这也是作为主流语言的必经之路惹
    def __init__(self, monkey: list[tuple[str, MONKEYSCRIPT]]):
        super().__init__([RR.REQUEST, RR.RESPONSE])
        self.monkey = monkey

    def request(self, flow):
        if not super().request(flow):
            return
        script=re.search(f"monkey/{TOKEN}-(.*)^",flow.request.url) # 拦截返回monkeyscript
        if script:
            try:
                with open(MONKEY_FOLDER+script.group(0),"rb",encoding="utf8") as f:
                    http.Response.make(200,f.read(),{"Content-Type":"application/javascript"})
            except:
                Ctx_gui.logger(f"script {script.group(0)} 不存在")


    def response(self, flow):
        if not super().response(flow):
            return
        print("MONKEY1")
        if "text/html" in flow.response.headers.get("content-type", ""):
            # 啥时候训练个AI专门识别混淆？
            # 对返回包带有text/html的包进行注入
            print("MONKEY2")
            rawhtml=Ctx_base.autocode(flow.response, flow.response.raw_content)
            ht=etree.HTML(rawhtml)
            hroot=ht.xpath("//html")[0]
            for f, m in self.monkey:
                if m == MONKEYSCRIPT.OUTSIDE:
                    _=etree.Element("script")
                    _.set("src",f"{TOKEN}-{f}")
                    hroot.append(_)
                with open(MONKEY_FOLDER+f, "r", encoding="utf8") as ff:
                    _=etree.Element("script")
                    _.text=ff.read()
                    if m == MONKEYSCRIPT.INNERHEAD:
                        hroot.insert(0,_)
                    elif m == MONKEYSCRIPT.INNERTAIL:
                        hroot.append(_)
            print("MONKEY")
            flow.response.text=etree.tostring(ht,encoding="utf8",pretty_print=True,method="html").decode("utf8")
