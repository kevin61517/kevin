"""
工廠模式
"""
from abc import ABC, abstractmethod


class Car(ABC):
    """汽車模組"""
    @abstractmethod
    def name(self):
        """行駛"""


class X1(Car):
    """Model X1"""
    def name(self):
        return 'BMW X1車款'


class X2(Car):
    """Model X2"""
    def name(self):
        return 'BMW X2車款'


class X3(Car):
    """Model X3"""
    def name(self):
        return 'BMW X3車款'


class Bmw:
    """ BMW 寶馬汽車公司"""
    def __init__(self):
        self._cars = {}

    def get_car(self, name) -> Car:
        if not self._cars.get(name):
            if name == 'x1':
                self._cars[name] = X1()
            elif name == 'x2':
                self._cars[name] = X2()
            else:
                self._cars[name] = X3()
        return self._cars[name]


class A:
    def __init__(self):
        self.a = 3
a = A()


if __name__ == '__main__':
    bmw = Bmw()
    car = bmw.get_car('x1')
    print(car.name())
    print(getattr(a, 'a', False))
