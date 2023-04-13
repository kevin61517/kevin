from .jml import *


async def main():
    print('== 登山抽籤爬蟲測試開始 ==')
    schedule = """D1:向陽派出所 -> 向陽山屋 -> 向陽登山口 -> 向陽山 -> 向陽登山口 -> 嘉明湖山屋
    D2:嘉明湖山屋 -> 三叉山 -> 嘉明湖 -> 三叉山 -> 嘉明湖山屋 -> 向陽山屋 -> 向陽派出所"""
    data = {
        'team_data': {
            'name': '快樂登山隊',
            'members': '2',
            'schedule': schedule,
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
            {
                'name': '劉善峻',
                'id': 'T124154315',
                'birth': '1998-09-22',
                'emergency_name': '劉德明',
                'emergency_tel': '0922117696'
            },
            {
                'name': '劉峻銘',
                'id': 'D122706130',
                'birth': '1995-04-02',
                'emergency_name': '姓名：劉明勇',
                'emergency_tel': '0928109465'
            },
            {
                'name': '曾弼凱',
                'id': 'A130328165',
                'birth': '1995-02-07',
                'emergency_name': '粘柚香',
                'emergency_tel': '0911286730'
            },
            {
                'name': '曾弼凱',
                'id': 'A130328165',
                'birth': '1995-02-07',
                'emergency_name': '粘柚香',
                'emergency_tel': '0911286730'
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
    await Jml(**data).start()
    print('== 登山抽籤爬蟲測試結束 ==')