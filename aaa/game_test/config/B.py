from game_test.config.interface import BaseConfig


class B_Game(BaseConfig):
    def __init__(self):
        self.pw = '000000'
        self.mchid = '99'

    def to_json(self):
        return {'pw': self.pw, 'mchid': self.mchid}
