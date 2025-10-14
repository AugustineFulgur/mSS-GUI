import threading

TOKEN="b05298d93a25" #TOKEN 未填写时随机生成

lock=threading.Lock()

# 单例写法比克苏鲁还扭曲这一块 多线程这一块
class Config:
    __instance__ = None
    __lock__ = threading.Lock()
    
    def __new__(cls):
        if cls.__instance__ is None:
            with cls.__lock__:
                if cls.__instance__ is None:
                    cls.__instance__ = super().__new__(cls)
                    #！！！此处定义全局变量！！！
                    cls.__instance__._data = {
                        "全局范围": "14.145.128.138",
                        "默认编码形式": "utf8", # UTF8 GBK... 为空时使用自动识别
                    }
        return cls.__instance__
    
    def get(self, key, default=None):
        with self.__lock__:
            return self._data.get(key, default)
    
    def set(self, key, value):
        with self.__lock__:
            self._data[key] = value
    
    def all(self):
        return self._data

# 使用单例
GLOBAL = Config()