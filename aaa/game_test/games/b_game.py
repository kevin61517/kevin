from game_test.games.interface import Interface


class B_Game(Interface):

    def __init__(self, pw, mchid):
        self.pw = pw
        self.mchid = mchid

    def pre_precess(self):
        print('== B pre_precess ==')

    def process(self):
        print('mchid===>', self.mchid)
        print('== B process ==')

    def post_process(self):
        print('== B post_process ==')