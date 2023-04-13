"""
策略模式
"""
from abc import ABC, abstractmethod


class BaseEquipment(ABC):
    @abstractmethod
    def exec(self):
        """策略"""


class Car(BaseEquipment):
    """車"""
    def exec(self):
        return '開車'


class Foot(BaseEquipment):
    """腿"""
    def exec(self):
        return '走路'


class ClassMate:
    """同學"""
    def __init__(self, name, equipment: BaseEquipment):
        self._name = name
        self._equipment = equipment

    def go_to_party(self):
        """前往派對"""
        return f'{self._name}{self._equipment.exec()}前往同學會。'


if __name__ == '__main__':

    Alice = ClassMate('Alice', Car())
    Bob = ClassMate('Bob', Foot())

    print(Alice.go_to_party())
    print(Bob.go_to_party())
