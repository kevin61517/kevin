from usdt import USDT


class ObjectSerializer:
    __object__ = None

    def as_object(self, **kwargs):
        if self.__object__:
            obj = {k: v for k, v in self.__dict__.items() if k in self.__object__.__dict__}
            print('self===>', self.__class__)
            print('__object__===>', self.__object__)
            print('s==>', self.__dict__.items())
            print('o==>', self.__object__.__dict__)
            if kwargs:
                obj.update(kwargs)
            return self.__object__(**obj)
        return None


if __name__ == '__main__':
    # u = USDT()
    # result = u.start()
    # print('result==>', result)

    def number_to_string(number: int or float, float_: int) -> str:
        """
        number: 預轉成字串的數字，可指定小數點後位數數量
        float_: 小數點位數
        return: str
        """
        setting_string = f'%.{float_}f'
        return setting_string % number

    print('===>', number_to_string(7.0700000123123123, 2))
