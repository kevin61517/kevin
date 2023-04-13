import abc


class InterFace(abc.ABC):
    @classmethod
    def __init_subclass__(cls, **kwargs):
        cls.name = cls.__name__

    def exec(self):
        """執行"""
        self.step_1()
        self.step_2()

    @abc.abstractmethod
    def step_1(self):
        """step 1"""

    @abc.abstractmethod
    def step_2(self):
        """step 2"""

    @classmethod
    def slots(cls):
        """slot"""
        print(cls.__slots__)
        print(cls.__dict__)
