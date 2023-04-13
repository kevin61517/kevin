from interface_test.interface import InterFace


class Leia(InterFace):
    """Leia"""

    def step_1(self):
        print(f'{self.name} -> 111')

    def step_2(self):
        a = {'School': 'NTU', 'Name': 'kevin'}
        b = {'Class': 'A', 'School': 'NSYSU'}
        a.update(b)
        print(a)
        print(f'{self.name} -> 222')