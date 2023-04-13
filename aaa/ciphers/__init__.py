"""
加密算法管理
調用Example:
    aes = cipher.aes(mode, key)
    message = aes.encrypt(data)
    cipher_text = message.result
"""
from .base import MethodType
from .aes import AESMessage, AES
from .rsa import RSA
from .base import Message, BaseCipher


class Ciphers:
    def __getattr__(self, name) -> MethodType:
        """算法呼叫口"""
        from .base import ALGORITHMS
        try:
            return ALGORITHMS[name.lower()].init
        except KeyError:
            raise NotImplementedError('Algorithms not implemented.')

    @staticmethod
    def algorithm(cls):
        from .base import ALGORITHMS
        if not isinstance(cls, type):
            raise TypeError('Algorithms object must be a class.')
        if not getattr(cls, 'init', None):
            raise TypeError('Algorithms object attribute "init" must implemented.')
        name = cls.__name__.lower()
        if ALGORITHMS.get(name):
            raise
        ALGORITHMS[name] = cls
        return cls


cipher = Ciphers()
