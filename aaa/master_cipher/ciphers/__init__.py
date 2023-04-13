"""
加密算法管理
調用Example:
    aes = cipher.aes(mode, key)
    message = aes.encrypt(data)
    cipher_text = message.result
"""
from .base import MethodType, Message
from .aes import AESMessage, AES
from .rsa import RSA


class Ciphers:
    def __getattr__(self, name) -> MethodType:
        """算法呼叫口"""
        from .base import ALGORITHMS
        try:
            return ALGORITHMS[name.lower()].init
        except KeyError:
            raise NotImplementedError('Algorithms not implemented.')


cipher = Ciphers()
