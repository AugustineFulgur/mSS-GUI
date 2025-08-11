from etc.base import *

class Ctx_head(Ctx_base):

    def __init__(self,head:dict, rr):
        super().__init__(rr)
        self.head=head