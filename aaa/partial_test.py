"""
new_a = partial(a, name='kevin')
右側的參數皆會以平時調用的方式來傳遞給左側的function。
"""
from functools import partial


def a(*args, **kws):
    print(args)
    print(kws)
    return 'success'


def b(c, name):
    print('c===>', c)
    print('name==>', name)
    return 'success'


new_a = partial(b, 1, 'kevin')

if __name__ == '__main__':
    print(new_a())
