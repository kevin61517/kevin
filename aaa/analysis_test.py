import sys
from PIL import Image
from mountain_crawlers.jml import Jml

data = {
    'team_data': {
        'name': '快樂登山隊',
        'members': '2',
        'schedule': '',
        'radio': '144270'
    },
    'member_data': [
        {
            'name': '楊開勻',
            'id': 'F128437592',
            'birth': '1992-08-12',
            'emergency_name': '楊遠波',
            'emergency_tel': '0921254089',
        },
        {
            'name': '曾弼凱',
            'id': 'A130328165',
            'birth': '1995-02-07',
            'emergency_name': '粘柚香',
            'emergency_tel': '0911286730'
        },
    ]
}

if __name__ == '__main__':
    picture = Image.open('captcha.png')
    method = sys.argv[1]
    print(dir(picture))
    print(picture.size)
    if not method:
        pass
    else:
        func = getattr(picture, method, '__str__')
        if callable(func):
            print('可呼叫')
            print(func((8, 6, 95, 45)).show())
        else:
            print('不可呼叫')
            print(func)
    cap = Jml(**data).analysis('captcha.png')
    print(cap)
