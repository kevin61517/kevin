"""計算機模組"""
"""
1.物件 x
2.裝飾器 x
"""


class Calculator:
    """計算機"""

    def add(self, x, y):
        return x + y

    def div(self, x, y):
        return x - y


if __name__ == '__main__':
    c = Calculator()
    a = c.add(3, 3)
    print(a)
