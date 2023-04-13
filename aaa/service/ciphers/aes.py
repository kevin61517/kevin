from abc import ABC

from attr import attrs, attrib
from .base import *
from Cryptodome.Cipher import AES as _AES
from Cryptodome.Util.Padding import pad, unpad
import base64

__ALGO__ = 'AES'


@attrs
class Encrypt(EncryptBase, algo_name=__ALGO__):
    """AES加密實作"""

    iv = attrib(default='112233')
    key = attrib(str, )

    def init_key(self):
        pass

    def init_cipher(self):
        return lambda s: s + f'==> aes {self.key} cipher'

    def exec(self, source):
        print('aes_en--->', self.key)
        print('aes_en--->', self.iv)
        return f'encrypt---> {source}'


@attrs
class Decrypt(DecryptBase, algo_name=__ALGO__):
    """AES解密實作"""

    iv = attrib(default='112233')
    key = attrib(str, )

    def init_key(self):
        print('== aes init key ==')
        pass

    def init_cipher(self):
        return lambda s: s + '==> aes cipher'


class __AES__(AlgorithmBase, algo_name=__ALGO__):
    """AES加密演算法"""
