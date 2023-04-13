import requests
from random import randint


class BasePeople:
    name = 'Aaa'


class P(BasePeople):
    def __init__(self):
        self.name = 'Kevin'

    def get_name(self):
        return self.name

    @classmethod
    def get_cls_name(cls):
        return cls.name


if __name__ == '__main__':
    u = [20, 29][randint(0, 1)]
    c = randint(10000, 900000)
    url = 'https://www.gate.io/json_svr/query_push'+f'/?u={u}&c={c}'
    payload = {'type': 'push_main_rates', 'symbol': 'USDT_CNY'}
    resp = requests.post(url=url, data=payload)
    print('resp===>', resp.json())
