import random
import sys


class Pokers:
    """撲克牌組"""

    def __init__(self):
        self._total = 52
        self._marks = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
        self._stamp: dict = {}
        self._used: dict = {}
        self._has_answers: dict = {}
        self._no_answers: dict = {}
        self._AMOUNT_OF_MARK = 4

    @property
    def used(self) -> dict:
        """已經使用的牌"""
        return self._used

    @property
    def last_cards(self) -> int:
        """剩餘牌數"""
        return self._total

    def new(self) -> None:
        """新建牌組"""
        self._total = 52
        self._marks = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
        self._stamp: dict = {}
        self._used: dict = {}
        self._has_answers: dict = {}
        self._no_answers: dict = {}

    def random_cards(self, amount: int) -> str:
        """隨機選牌"""
        if amount > self._total:
            return '牌數不夠了！'
        self._total -= amount
        return ','.join(self._get_random_cards(amount))

    def _get_random_cards(self, amount: int) -> list:
        """隨機抽牌"""
        marks = []
        while amount:
            min_ = int(0)
            max_ = int(len(self._marks) - 1)
            mark = self._marks[random.randint(min_, max_)]
            used = self._used.get(mark, 0)
            if used == self._AMOUNT_OF_MARK:
                continue
            marks.append(mark)
            self._stamp[mark] = self._stamp.get(mark, 0) + 1
            self._used[mark] = used + 1
            amount -= 1
        return marks

    def set_used_to_cards(self):
        """使用過的牌從新洗牌"""
        marks = []
        total = 0
        for mark, amount in self._no_answers.items():
            marks.append(mark)
            total += amount
        self._marks = marks
        self._total = total

    def is_answer(self, has_answer: bool):
        """是否有解"""
        memo = {**self._has_answers} if has_answer else {**self._no_answers}
        for mark, value in self._stamp.items():
            memo[mark] = memo.get(mark, 0) + value
        self._used = memo
        self._stamp = {}


class PokersV2:
    def __init__(self):
        self._marks = {'s': '♠', 'h': '♥', 'd': '♣', 'c': '♦'}
        self._numbers = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
        self._cards: dict[str:tuple] = {}
        self._used: dict = {}

    def new(self):
        """新牌組"""
        for number in self._numbers:
            self._cards[number] = [mark for mark in self._marks.values()]

    @property
    def cards(self) -> dict:
        """查看牌組"""
        return self._cards

    def random_cards(self, amount: int):
        """隨機抽牌"""


pokers = Pokers()
pokersv2 = PokersV2()
pokersv2.new()


def test():
    p = PokersV2()
    p.new()
    assert 1==1


def play_game():
    print('== play ==')
    print('剩餘牌數：', pokers.last_cards)
    while pokers.last_cards:
        cards = pokers.random_cards(4)
        print(cards)
        has_ans = input('是否有解？[Y|N]')
        pokers.is_answer(True if has_ans.lower() == 'y' else False)
    ans = input(f'目前剩下{pokers.last_cards}張牌，是否重洗使用過的牌？[Y|N]')
    if ans == 'y':
        pokers.set_used_to_cards()
        return play_game()
    print('謝謝遊玩！')


class PokerGame:
    def __init__(self):
        self.times = 4
        self.total = 52
        self.marks = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
        self.used: dict = {}
        self.no_answer = {}

    def new_game(self):
        """新遊戲"""
        self.used: dict = {}
        self.total = 52

    def get_cards(self):
        """取得牌組"""
        cards = []
        if self.total:
            for time in range(self.times):
                index = random.randint(0, 12)
                card = cards[index]
                used = self.used.get(card, 1)
                if used == 4:
                    continue
                self.used[card] = used + 1
            self.total -= 4
            yield cards
        return '沒牌了！'


if __name__ == '__main__':
    print(pokersv2.cards)
    # play_game()
    # try:
    #     nums = sys.argv[1]
    # except:
    #     nums = 4
    # print(pokers.random_cards(nums))
    # print(pokers.used)
