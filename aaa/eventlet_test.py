import eventlet
import time
from datetime import datetime, timedelta, timezone
import re
from delorean import Delorean, parse

LOCAL_TZ = 'Asia/Shanghai'


def a():
    time.sleep(1)
    print('== a ==')


def b():
    time.sleep(1)
    print('== b ==')


def c():
    time.sleep(1)
    print('== c ==')


_iso8601_regex = re.compile(
    r'^(-?(?:[1-9][0-9]*)?[0-9]{4})-(1[0-2]|0[1-9])-(3[01]|0[1-9]|[12][0-9])T(2[0-3]|[01][0-9]):([0-5][0-9]):([0-5][0-9])(\.[0-9]+)?(Z|[+-](?:2[0-3]|[01][0-9]):[0-5][0-9])?$'
)


def validate_iso8601(s):
    return _iso8601_regex.match(s)


def parse_time(s, tz=LOCAL_TZ) -> Delorean:
    """
    处理时间字符串，转换为 Delorean 时间对象
    :param s: 时间字符串
    :param tz: 时区信息
    :return:  Delorean
    """
    if validate_iso8601(s):
        return parse(s, dayfirst=False)
    return parse(s, dayfirst=False, yearfirst=True, timezone=tz)


def parse_dr(value, sep='~'):
    """日期范围"""
    if sep not in value:
        return None
    start, end = [i.strip() for i in value.split(sep)]
    start = parse_time(start).shift('UTC').datetime
    end = parse_time(end).shift('UTC').datetime
    print(start, end)


if __name__ == '__main__':
    query = {'created_dr': '2022-07-03 00:00:00 ~ 2022-07-03 23:59:59'}
    parse_dr(query['created_dr'])
    day = 1
    yesterday = datetime.utcnow().astimezone() - timedelta(days=day)
    print('yesterday: ', yesterday)
    print('yesterday-start: ', Delorean(datetime=yesterday).start_of_day - timedelta(days=day))
    print('yesterday-end: ', Delorean(datetime=yesterday).end_of_day + timedelta(days=day))
    print((datetime.utcnow() - timedelta(days=1)).date())
    print(datetime.utcnow())
    # print((datetime.utcnow() - timedelta(days=1)).date())
