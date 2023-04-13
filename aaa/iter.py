class Iter:

    types_ = {
        'int': True,
        'str': True
    }

    def __init__(self):
        self.__container = [1, 2, 3]

    def __iter__(self):
        for i in self.__container:
            yield i

    def __class_getitem__(cls, *args, **kws):
        print(args, kws)
        return

    def __contains__(self, key) -> bool:
        return bool(self.types_.get(key, 0))

    def __setitem__(self, key, value):
        return


if __name__ == '__main__':
    it = Iter()
    print(property)
    print('int' in it)
    for i in it:
        print(i)