import attr
import types
from ciphers import cipher


@attr.s(slots=True, kw_only=True)
class Conf:
    url: str = attr.ib(default='https://yl82hg-esbo.inplaymatrix.com/backoffice/default.htm')
    username: str = attr.ib(default="YL82HG")
    password: str = attr.ib(default="asdf1234")


class A(Conf):
    @classmethod
    def do(cls):
        print('dict====>', cls.__dict__)
        print('slots===>', cls.__slots__)
        print(getattr(cls, '__slots__', cls.__dict__))


@cipher.algorithm
class AAA:
    def __init__(self, key):
        self._key = key

    @classmethod
    def init(cls, key):
        return cls(key=key)

    @property
    def key(self):
        return self._key


if __name__ == '__main__':
    A.do()
    c = cipher.aes(mode=1, key='abcd123456780000')
    message = c.encrypt('kevin')
    o = cipher.aaa('abcd1234')
    print(o.key)
