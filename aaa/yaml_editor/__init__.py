import yaml
from payment.env import root
from .tools import format_name, str_to_list, try_input_int, try_input_char
from typing import List

from .spec import spec_edit
from .merchants import merchants_edit
from .gateway import gateway_edit, Gateway


def make_yaml(gateway_name: str):
    """
    生成yaml
    gateway_name: 網關中文名稱
    """
    _format = format_name()
    # 編輯網關
    gateway: dict = gateway_edit(gateway_name=_format(gateway_name))
    # 編輯spec
    spec: dict = spec_edit(gateway_type=gateway['type'])
    # 編輯商戶
    merchants: List[dict] = merchants_edit(gateway_name=gateway_name, gateway_type=gateway['type'])
    with open(f'{root(".")}/config/{gateway["gateway"].lower()}.yaml', 'w') as file:
        yaml.dump(
            {**gateway, 'spec': spec, '_merchants': merchants},
            file,
            sort_keys=False,
            explicit_start=True,
            allow_unicode=True,
            encoding='utf8'
        )
