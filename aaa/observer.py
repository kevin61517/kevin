class FunctionQueue:
    def __init__(self, lst: list = None):
        self.__connects = lst or []

    @property
    def queue(self):
        return self.__connects


class Observer:

    queue = FunctionQueue

    def __init__(self):
        self.__connects = self.queue()

    def connect(self, func):
        self.__connects.queue.append(func)
        return func

    def send(self, *args, **kws):
        for func in self.__connects.queue:
            func(*args, **kws)


class Before(Observer):
    """"""


class After(Observer):
    """"""


class ObserverManager:

    def __getitem__(self, item):
        return self.__dict__[item]

    @classmethod
    def init(cls):
        """"""
        instance = cls()
        for obs in Observer.__subclasses__():
            setattr(instance, obs.__name__.lower(), obs())
        return instance


observer = ObserverManager.init()
print(observer['before'])
before = Observer()
after = Observer()


@before.connect
def a(name) -> None:
    print('Before', name)


@after.connect
def b(name) -> None:
    print('After', name)


def main(name: str):
    message = 'print ' + name
    before.send(message)
    print(f'== {message} ==')
    after.send(message)


if __name__ == '__main__':
    main('kevin')
