# import attr
# import yaml
#
# from service import *
# from attr import attrs, attrib, NOTHING
# from typing import NewType
# from service.ciphers2 import cipher
# import json
# # === AES ===
# from Cryptodome.Cipher import AES
# from Cryptodome.Util.Padding import pad, unpad
# import base64
# # === AES ===
# import os
# import sys
# from collections import deque
# from abc import ABC, abstractclassmethod, abstractmethod, abstractproperty
# from slugify import slugify
# from glob import glob
# import re
# import os
# from pathlib import Path
import hmac
# import hashlib
# import requests
# import subprocess
# import structlog
#
# # # if the script don't need output.
# # subprocess.call("php /path/to/your/script.php")
# #
# # # if you want output
# # proc = subprocess.Popen("php /path/to/your/script.php", shell=True, stdout=subprocess.PIPE)
# # script_response = proc.stdout.read()
#
# get_logger = structlog.get_logger()
from decimal import Decimal
import re
import requests
import sys
import os
import attr
import json
from types import FunctionType
import asyncio
import time
from attr import Factory, attrib, attrs
from datetime import datetime, timezone, timedelta, date
from delorean import Delorean
import pytz
from random import randint
import json

pattern = r'^(http|https):\/\/([\w\d + (\-)+?]+\.)+[\w]+(\/.*)?$'
IP_PATTERN = r'^[0-9]*$'


def str_to_list(s):
    return [element for element in s.replace(' ', '').split(',') if element]


def _set_api(retry=False):
    """設置api"""
    if not retry:
        print('說明：下單網關[支付填寫HOST+API|代付填寫HOST]')
    v: str = input('設置：')
    if not re.match(pattern, v):
        print(f'地址 {v} 不符合規格，請重新填寫。')
        return _set_api(retry=True)
    return v


def _set_white_list(retry=False):
    """設置ip"""
    if not retry:
        print('說明：回調IP白名單, IP之間以,做為分隔。Ex:a, b, c, d')
    ips = str_to_list(input('設置：'))
    for ip in ips:
        if not re.match(IP_PATTERN, ip.replace('.', '')):
            print(f'IP {ip} 不符合ip規格，請重新輸入。')
            return _set_white_list(retry=True)
    return ips


# d = {'partner_id': ['11880032'], 'channel_id': ['51'], 'partner_order': ['123456790'], 'user_id': ['1'], 'order_id': ['20211222021000497935'], 'total_fee': ['20000'], 'real_money': ['20000'], 'success_time': ['2021-12-22 13:26:05'], 'code': ['1001'], 'sign': ['0104fa3954503e7f42de12c3a3521366']}

def named():
    name = input('設置姓名：')
    if 'a' not in name:
        print('a必須存在於姓名中!!')
        return named()
    return name


def classed():
    class_ = input('設置班級：')
    if class_ not in ['A', 'B', 'C']:
        print('班級必須是A, B, C')
        return classed()
    return class_


# d = {
#     'name': named(),
#     'class': classed()
# }

ddd = {'memberid': ['211308499'], 'orderid': ['1234567898'], 'transaction_id': ['202112241050537441631009853996'], 'amount': ['499.0000'], 'datetime': ['20211224105544'], 'returncode': ['00'], 'sign': ['F30774A3C48C9D0EA5C072A42F28521D']}


def _set_json_arguments(prompt_message='', init_sign=True) -> list:
    """
    設置多個參數，for json格式資料。
    prompt_message: 提示訊息
    init_sign: 實例化簽名
    """
    f_map = {
        'i': 'int',
        'd': 'Decimal',  # 裝飾器: 位數n，回傳有n為小數點的實作方法。
        's': 'str',
        'f': 'float'
    }
    map_ = {
        '商戶號': 'cfg.appid',
        '商戶密鑰': 'cfg.appsecret',
        '回調地址[同步|異步]': 'cfg.callback_url',
        '商戶訂單號': 'order.order_no',
        '訂單金額': 'order.amount',
        '使用者ID': 'order.userid',
        '使用者IP': 'order.client_ip',
        '整數時間戳記': '填寫位數。Ex: timeU=10',
        '普通時間戳記': '填寫格式。Ex: timeP=YYYYMMDDhhmmssff'
    }
    print(f'== 設置{prompt_message} ==')
    print('說明：')
    print('1.先輸入所需參數數量\n', '2.用 = 來表示參數對應值。\n', '3.用 # 來表示參數的類型[i=整數, f=浮點數, s=字串]。', sep='')
    print('完整範例：', 'amount=order.amount=i\n', 'timestamp=timeP=YYYY-MM-DD hh-mm-ss-ff', sep='')
    n: int = int(input('參數數量：'))
    result = []
    for i in range(1, n+1):
        f, v, fmt = 0, 1, 2
        data = input(f'設置第 {i} 個參數：').split('=')  # key, value, format
        field, value, format_ = data[f], data[v], f_map[data[fmt]]
        print(field, value, format_)
        if value.startswith('!!'):
            result.append({'field': field, 'type': 'SignField', 'init': init_sign})
        else:
            result.append({'field': field, 'valuer': f'{format_}({value})'})
    return result


def month(house_rent, deposit, month_income):
    def _in(*day_outcomes):
        month_outcome = int(sum(day_outcomes)) * 30
        return int(month_income - month_outcome - house_rent - deposit)
    return _in


def day(day_max):
    def _in(*outcomes):
        return int(day_max - sum(outcomes))
    return _in


class Test:
    def __init__(self, secret_key):
        self.query_url = 'http://bochat.dev.api/bj/apis/v1/cs_url'
        self.secret_key = secret_key

    def exec(self, _business_key, msg):
        data = self._body(msg)
        url = self.url_for(_business_key)
        resp = self._request(url, data)

    @staticmethod
    def url_for(business_key):
        return f'https://api.bx4391.com/b/apis/v1/business/{business_key}/notification'
        # return f'https://bochat-api.iyes.dev/b/apis/v1/business/{business_key}/notification'

    @staticmethod
    def _request(url, payload):
        headers = {'Content-Type': 'application/json'}
        resp = requests.post(url, json=payload, headers=headers)
        print('返回：', resp.content, resp.status_code)
        return resp

    def _body(self, msg):
        cipher_text = self._encode(msg)
        data = {
            "message": msg,
            "secret": cipher_text,
            "created_at": int(time.time())
        }
        return data

    def _encode(self, msg):
        cipher_text = hmac.new(key=self.secret_key.encode(), msg=msg.encode(), digestmod='sha256')
        r = cipher_text.hexdigest()
        print('加密訊息：', r)
        return r


t = Test(secret_key='rVk8Ehw2UMBevDbXGyrkeykmzagPm6dD')


async def work(num):
    await asyncio.sleep(2)
    print(f'== 工作 {num} 已完成 ==')
    return num


async def main():
    print('== 開始測試 ==')
    work1 = await work(1)
    print('111')
    work2 = await work(2)
    print('222')
    work3 = await work(3)
    print('333')


def pay_methods(p_mth):
    mth = f'{p_mth}'
    if mth in ('0', 'redirect'):
        return 'redirect'
    elif mth in ('1', 'qrcode'):
        return 'qrcode'
    elif mth in ('2', 'bank'):
        return 'bank'
    elif mth in ('3', 'form-post'):
        return 'form-post'
    else:
        return 'redirect'


def test(*num):
    print(type(num))


@attrs(slots=True, frozen=True)
class Credential:
    type: str = attrib(converter=pay_methods)  # 凭证类型, redirect,bank,qrcode
    test: str = attrib()


def cal(rows):
    d = {}
    result = []
    for row in rows:
        if row.get('name', '') not in d.keys():
            d[row['name']] = row
        else:
            d[row['name']]['number'] += row['number']
    return d


def phone(_phone):
    if '0' not in _phone:
        print('我在不合格的電話')
        raise ValueError('不合格的電話')
    return _phone


def mail(_mail):
    if '@' not in _mail:
        print('我在不合格的電子信箱')
        raise ValueError('不合格的電子信箱')
    return _mail


def v_ali(account, valid):
    try:
        return valid(account)
    except:
        return False


def aaa():
    result = (i for i in range(10))
    yield from result


def start_of_day(time_, tz_='Asia/Shanghai'):
    """
    获取当日UTC时间的本地起始日期
    :param time_:
    :param tz_:
    :return:
    """
    return Delorean(time_, timezone='UTC').shift(tz_).start_of_day


if __name__ == '__main__':
    from dateutil.parser import parser
    from collections import deque
    c = Credential(
        type=sys.argv[1],
        test='1'
    )
    LOCAL_TZ = 'Asia/Shanghai'
    now = Delorean(timezone=LOCAL_TZ).datetime.replace(microsecond=0).astimezone(pytz.UTC)
    print(now)
    print(Delorean(datetime=now).start_of_day)#.replace(microsecond=0).astimezone(pytz.UTC) + timedelta(days=1))
    today = datetime.utcnow().astimezone()
    start = Delorean(datetime=today).start_of_day - timedelta(days=2)
    end = Delorean(datetime=today).end_of_day
    amount = 30000
    meal = 300 * 30
    traffic = 1500
    house = 14000
    print('餐費：', meal)
    print('交通：', traffic)
    print('房租：', house)
    print(amount - meal - traffic - house)
    aa = [1, 2, 3]
    bb = [1, 2, 3]
    print(map(lambda a: a, zip(aa, bb)))
    # for i in map(lambda a: a, zip(aa, bb)):
    #     print(i)
    d = '{"code":40001,"message":"\u8bf7\u8f93\u5165\u8d44\u91d1\u5bc6\u7801","payload":{"failure_code":40001,"failure_msg":"\u8bf7\u8f93\u5165\u8d44\u91d1\u5bc6\u7801"},"type":"invalid_request"}'
    print(json.loads(d))
    # for i in zip(aa, bb):
    #     print(i)
    # _a = aaa()
    # print(_a)
    # for i in _a:
    #     print(i)
    LOCAL_TZ = 'Asia/Shanghai'
    print(datetime.utcnow().replace(microsecond=0))
    print(datetime.utcnow().replace(microsecond=0).replace(tzinfo=timezone.utc))
    data = {
        'times_1': [('kevin69', Decimal('1')), ('69kevin', Decimal('1')), ('master69', Decimal('1'))],
        'times_2': [],
        'times_5': [],
        'times_10': [],
        'times_30': [],
        'times_50_up': []
    }
    print([v for v in data.values()])

    def f(a=None, b=None, c=None):
        return [a, b, c]
    # m = map(*[v for v in data.values()])
    aa = [1, 2, 3]
    bb = [1, 2]
    cc = [1, 2]

    class o:
        def __init__(self, num):
            self.deposit_times = num
    o1 = o(1)
    o2 = o(2)
    o3 = o(3)
    data = [o1, o2, o3]

    def package(origin):
        if not isinstance(origin, deque):
            origin = deque(origin)
        keys = ['times_1', 'times_2', 'times_5', 'times_10', 'times_30', 'times_50']
        max_try = len(origin)
        r = {}
        while max_try > 0:
            max_try -= 1
            obj = origin.pop()
            key = f'times_{obj.deposit_times}'
            if key not in keys:
                continue
            elif key in keys and not r.get(key):
                r[key] = obj
            else:
                origin.appendleft(obj)
        return r, origin

    result = []
    while data:
        print('data:', data)
        r, data = package(data)
        result.append(r)
    import time
    from datetime import datetime
    start = datetime.now()
    end = datetime.now()
    print(end - start)
    origin = {'name': 'kevin'}
    new = {'numbers': {'1': True, '2': True}}
    print({**origin, **new})
    s = ''
    r = s.replace(' ', '').split(',')
    if len(r) == 1 and not r[0]:
        r.pop()
    d = {k: True for k in r}
    print(','.join(['1', '2', '3']))
    s = '1'
    print(s[:-1])
    tz = LOCAL_TZ = 'Asia/Shanghai'
    # get_start_time
    init_start = Delorean(timezone=tz).start_of_day.astimezone(pytz.UTC) - timedelta(days=int(1))
    print('報表啟動的時間戳(當前日期-1天後轉UTC)[-----------]：', init_start)
    start = start_of_day(init_start)
    print('報表計算的時間戳(當前日期-1天候去UTC)[用作created]：', start)


# class A:
#
#     fields = ['total_claim_approve', 'total_approved_times', 'total_reversed_times', 'average_time_claim_approve',
#               'average_time_operation']
#     data = staff_transfer_stats_daily.get_total_datas(fields, filters)
#
#     def get_field(self, fields):
#         expr = []
#         for field in fields:
#             expr.append(
#                 func.sum(func.IF(getattr(self.__model__, field) != 0, getattr(self.__model__, field), 0)).label(field)
#             )
#             if field.startswith('average'):
#                 expr.append(
#                     func.sum(func.IF(getattr(self.__model__, field) != 0, 1, 0)).label(f'{field}_count')
#                 )
#         return expr
#
#     def get_total_datas(self, fields: list, filters):
#         d = db.session.query(
#             *self.get_field(fields),
#         ).filter(*self.to_filter(filters)).one()
#         data = dict(
#             zip(
#                 fields,
#                 [int(getattr(d, field) or 0) // int(getattr(d, f'{field}_count') or 1)
#                  if field.startswith('average') else int(getattr(d, field) or 0) for field in fields]
#             ))
#         return data
"""
出發日期：
2022/04/01 (六) 20:00
結束日期：
2022/04/04 (一) 20:00
==========
姓名：楊開勻
身分證：F128437592
生日：1992-08-12
手機：0988771279
地址：台北市信義區忠孝東路五段717號4樓
==========
姓名：曾弼凱
身分證：A130328165
生日：1995-02-07
手機：0910970207
地址：台南市東區中華東路二段193號9-11
jbk1995kb@gmail.com
==========
姓名：程尉慈
身分證：P223754373
生日：1995-02-09
手機：0911446205
地址：台南市東區中華東路二段193號9-11
==========
姓名：姜韋辰
身分證：H125009329
生日：1997-09-28
手機：0926548510
地址：桃園市龍潭區九龍里五福街243巷93號
==========
"""

