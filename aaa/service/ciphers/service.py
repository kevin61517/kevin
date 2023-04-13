from .base import ALGORITHMS


class Ciphers:
    def __getattr__(self, name):
        try:
            return ALGORITHMS[name]
        except KeyError:
            raise NotImplementedError(f'Algorithm {name} not implemented.')

    @staticmethod
    def algorithms():
        return [algo for algo in ALGORITHMS.keys()]


ciphers = Ciphers()
