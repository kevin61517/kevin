from interface_test.interface import InterFace


class Kevin(InterFace):
    """Kevin"""

    def step_1(self):
        print(f'{self.name} -> 111')

    def step_2(self):
        print(f'{self.name} -> 222')
