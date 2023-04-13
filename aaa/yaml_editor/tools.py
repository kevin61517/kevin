import os
import string
from slugify import slugify
from typing import List, Union
import re

API_PATTERN = r'^(http|https):\/\/([\w\d + (\-)+?]+\.)+[\w]+(\/.*)?$'
IP_PATTERN = r'^[0-9]*$'


def str_to_list(s):
    return [element for element in s.replace(' ', '').split(',') if element]


def format_name(rename=None):
    """格式化名稱"""
    def _new(chinese_name):
        # 中文轉羅馬拼音(wan-hai-zhi-fu)
        name = slugify(chinese_name)
        # 格式化(wanhaizhifu)
        new_name = name.title().replace('-', '')
        # 檢查是否已存在相同名稱
        if os.path.isfile(f'./config/{new_name}.yaml'):
            return rename(new_name) if rename else ''.join([word[0] for word in name.split('-')])
        return new_name
    return _new


def try_input_int(msg: str) -> int:
    v = input(msg)
    try:
        return int(v)
    except:
        print(f'>> 參數輸入錯誤({v}不是一個整數類型參數) <<')
        return try_input_int(msg)


def try_input_char(msg: str) -> str:
    v = input(msg)
    if v not in string.ascii_lowercase:
        print(f'>> 參數輸入錯誤({v}不是一個英文字母) <<')
        return try_input_char(msg)
    return v
