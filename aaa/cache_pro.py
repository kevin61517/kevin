import time


class cached_property:
    """ 缓存实例属性 """

    def __init__(self, factory):
        self._attr_name = factory.__name__
        print('_attr_name==>', self._attr_name)
        self._factory = factory

    def __get__(self, instance, owner):
        print('instance:', instance)
        attr = self._factory(instance)
        setattr(instance, self._attr_name, attr)
        return attr


class A:
    @cached_property
    def test(self):
        print('111')
        return 'name'


a = A()

def abcd():
    pass


if __name__ == '__main__':
    print(abcd.__name__)
    while True:
        print(a.test)
        time.sleep(1)
