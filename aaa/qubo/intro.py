"""
趣播流程圖
用途：給 [趣播] 配置下載包的管理後台。
功能：
 - 配置域名與下載包：讓 [趣播] 運營人員可以配置域名與該域名存放的下載包。
 - 新增模板：前端管理。
 - API開發：後端管理。

產品流程圖
         ____ aaa.com?queryAgent ____                ___ aaa.com：下載包A
        ｜                           ｜             ｜                   \_______
User -->         [ 域名邏輯 ]          --  SERVER -->    [下載包配置邏輯]  /       ｜
 ｜     ｜____ bbb.com?queryQubo ____｜             ｜___ bbb.com：下載包B        ｜
 ｜                                                                             ｜
 ｜                                                                             ｜
  ---------------------<------------------<-----------------<-------------------
"""
from functools import wraps
#
# def multi_wallet(service_name='accounts'):
#
#     def _mid(method):
#         def _wrapper(currency='CNY', *args, **kws):
#             # from spinach.services import accounts, account_multi
#             if currency == 'CNY':
#                 return method(*args, **kws)
#                 # return getattr(accounts, method.__name__)(*args, **kws)
#             from spinach.services import account_multi
#             return getattr(account_multi, method.__name__)(*args, **kws)
#         return _wrapper
#     return _mid


class Main:
    def __getattr__(self, name):
        if not hasattr(self, name):
            return self.__a(name)

    def __a(self, name):

        def func(*args, **kwargs):
            currency = kwargs.get('currency')
            service = getattr(accounts, name)
            if currency == 'CNY':
                from spinach.service import accounts
                obj = getattr(accounts, name)(*args, **kwargs)
            elif currency == 'USDT':
                from spinach.service import account_mutis
                obj = getattr(account_mutis, name)(*args, **kwargs)
        return func


def multi_wallet(method):
    @wraps(method)
    def _in(*args, **kws):
        print(isinstance(args[0], AccountService))
        print('args[0]===>', args[0])
        print('args-->', args)
        print('kws--->', kws)
        print(method.__dict__)
    return _in


class Account:
    name: str
    number: int


class AccountMulti: ...


class AccountService:
    __model__ = Account

    @multi_wallet
    def get(self, aa, bb):
        return 1


class AccountMultiService:

    def get(self):
        print('self.__class__===>', self.__class__)
        print('self.__dict__===>', self.__class__.__dict__)
        return 2


class Manager:
    def __init__(self):
        """"""

    def run(self, *tasks):
        for task in tasks:
            task()


def prod():
    yield from range(10)


def consumer():
    while 1:
        data = yield
        print(f'消費了{data}號商品')


def main(prd, con):
    pr = prd()
    co = con()
    next(co)
    for p in pr:
        co.send(p)


class Context:
    def __init__(self):
        self.name = 'i am context'

    def __enter__(self):
        print('== ENTER ==')
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        print('exc_type===>', exc_type)
        print('exc_val====>', exc_val)
        print('exc_tb=====>', exc_tb)


context = Context()


if __name__ == '__main__':
    main(prod, consumer)
