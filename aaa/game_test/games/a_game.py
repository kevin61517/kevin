from game_test.games.interface import Interface


class A_Game(Interface):
    def __init__(self, code, username):
        self.code = code
        self.username = username

    def pre_precess(self):
        print('== A pre_precess ==')

    def process(self):
        print('usernam===>', self.username)
        print('== A process ==')

    def post_process(self):
        print('== A post_process ==')