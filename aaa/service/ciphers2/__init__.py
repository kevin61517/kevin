from .base import ALGORITHMS
from .aes import *


class Ciphers:

    def __getattr__(self, name):
        try:
            return ALGORITHMS[name].init
        except KeyError:
            raise NotImplementedError('Algorithms not implemented.')


cipher = Ciphers()
