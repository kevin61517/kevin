from abc import ABC

from attr import attrs, attrib
from .base import *

__ALGO__ = 'RSA'


@attrs
class Encrypt(EncryptBase, algo_name=__ALGO__):
    key: str = attrib(str, )

    def init_key(self):
        pass

    def init_cipher(self):
        return lambda s: s + f'==> aes {self.key} cipher'


@attrs
class Decrypt(DecryptBase, algo_name=__ALGO__):
    key: str = attrib(str, )

    def init_key(self):
        pass

    def init_cipher(self):
        return lambda s: s

    def exec(self, source):
        print('de--->', self.key)
        return f'decrypt---> {source}'


class RSA(AlgorithmBase, algo_name=__ALGO__):
    pass
