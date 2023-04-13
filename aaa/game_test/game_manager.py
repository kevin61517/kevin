"""
遊戲統一管理
"""

from game_test.games.interface import Interface
from game_test.config.interface import BaseConfig


class ConfigManager:
    def __init__(self):
        self.configs: dict = {}

    def init(self):
        print('configs===>', BaseConfig.__subclasses__())
        for config in BaseConfig.__subclasses__():
            self.configs[config.__name__.lower()] = config()

    def get_config(self, name):
        config = self.configs.get(name, None)
        if not config:
            raise ValueError('Config Not Found!')
        return config

    def c(self):
        print('已註冊配置：', self.configs)


configs = ConfigManager()
configs.init()  # 初始化配置管理
configs.c()


class GameService:
    def __init__(self):
        self._register: dict = {}

    def init(self):
        for game in Interface.__subclasses__():
            name = game.__name__.lower()
            config: BaseConfig = configs.get_config(name)
            self._register[name] = game.init(**config.to_json())

    def get_game(self, name) -> Interface:
        service = self._register.get(name)
        if not service:
            raise ValueError('Game Not Found!')
        return service


game_service = GameService()
game_service.init()
