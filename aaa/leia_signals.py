# Signals factory
class Signals:
    def __init__(self, name):
        self.signal_name = name
        self.listeners = []

    def connect(self, function):
        self.listeners.append(function)
        return function

    def send(self, *args, **kws):
        for listener in self.listeners:
            listener(*args, **kws)


# create signal
user_updated = Signals('user.updated')


# signal connect
@user_updated.connect
def aaa(caller):
    """do something when updated user"""
    print(f'{caller} calling me to do something...')
    print('===> Start doing aaa!')


@user_updated.connect
def bbb(caller):
    """do something when updated user"""
    print(f'{caller} calling me to do something...')
    print('===> Start doing bbb!')


# signal send
def start_updated_user():
    print('== Update User ==')
    user_updated.send(caller='leia')


if __name__ == '__main__':
    # start test
    start_updated_user()
