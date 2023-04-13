from attr import attrs, attrib, define


@attrs(slots=True)
class Obj:
    number = attrib()
    name = attrib()
    cls = attrib(default='A')

    @name.default
    def _name(self):
        print(self)
        return 'kevin'

    @name.validator
    def _v(self, _, value):
        if not isinstance(value, int):
            print('== 驗證失敗 ==')


@define(kw_only=True)
class A:
    name = attrib()


if __name__ == '__main__':
    o = Obj('14')
    print(o.name)
    # obj = Obj('kevin', 14)
    # print(obj)
    # print(A(name='kevin'))
    # k = None
    # print(k.__class__.__module__)
