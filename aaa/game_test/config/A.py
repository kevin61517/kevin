from game_test.config.interface import BaseConfig


class A_Game(BaseConfig):
    def __init__(self):
        self.code = '123456'
        self.username = 'joki_test'

    def to_json(self):
        return {'code': self.code, 'username': self.username}
