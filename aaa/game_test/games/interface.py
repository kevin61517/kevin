"""
規範遊戲物件行為
"""


class Interface:

    def launch(self):
        self.pre_precess()
        self.process()
        self.post_process()
        return 'success'

    def pre_precess(self):
        raise NotImplementedError

    def process(self):
        raise NotImplementedError

    def post_process(self):
        raise NotImplementedError

    @classmethod
    def init(cls, **kws):
        return cls(**kws)

