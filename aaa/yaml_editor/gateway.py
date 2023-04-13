import re
from attr import attrs, attrib, NOTHING
from .tools import str_to_list, try_input_int, API_PATTERN, IP_PATTERN, List
from payment.constants import CALLBACK_URLS, CURRENCIES


@attrs
class Gateway:
    """
    網關字段
    沒有[default]值的參數會被編輯
    """

    prompt_message = '網關參數'

    # 0 支付类别，1 代付类别
    type = attrib(metadata={'msg': '第三方類型[0=支付, 1=代付]'}, converter=int)
    # 下單地址
    api = attrib(metadata={'msg': '下單網關[支付填寫HOST+API|代付填寫HOST]'})
    # 回调白名单列表
    whitelist = attrib(
        type=list,
        metadata={'msg': '回調IP白名單, IP之間以,做為分隔。Ex:a, b, c, d'},
        converter=str_to_list
    )
    # 类名
    gateway = attrib(default='網關參數')
    # 回调地址
    callback_url = attrib(default="{host}/api/payment/callback/{gateway}")
    # 强制启用回调域名使用 https
    _force_https = attrib(default=False)
    # 备注说明
    note = attrib(default='')
    # 订单过期时间，分钟单位
    expires = attrib(default=15)
    # 精度位数，RMB=2，USDT=6
    decimals = attrib(default=2)
    # 随机小数位, 0 为不开启
    random_decimals = attrib(default=0)
    # 币种类型: 0 RMB, 1 USDT_ERC20, 2 USDT_TRC20
    currency = attrib(default='RMB')
    # 支付类别: 0 微信, 1 支付宝, 2 银联转账, 3 银行卡, 4 加密货币
    pay_type = attrib(default=0)
    # 付款方式: 0 跳转, 1 二维码, 2 银行卡
    pay_method = attrib(default=0)
    # -
    user_rating = attrib(default=0)
    # 输入金额类别， 0 任意输入, 1 固定输入
    amount_type = attrib(default=0)
    # 接受最小存款
    amount_min = attrib(default=1)
    # 接受最大存款
    amount_max = attrib(default=999999999)
    # 固定金额列表
    amount_fixed = attrib(type=list, default=[50, 100, 200])
    # 需要补充的存款人信息
    payer_cred = attrib(default={})
    # 支付需要的参数
    extra = attrib(default={})

    @classmethod
    def edit(cls):
        """編輯"""
        print(f'== 設置{cls.prompt_message} ==')
        data = {}
        for a in cls.__attrs_attrs__:
            if a.default == NOTHING:
                print(f'說明: {a.metadata["msg"]}')
                data[a.name] = input('設置: ')
        return cls(**data)

    def value(self) -> dict:
        return {a.name: getattr(self, a.name) for a in self.__attrs_attrs__}


def gateway_edit(gateway_name) -> dict:
    print('== 設置網關參數 ==')
    gateway_type: int = _set_type()
    data = {
        'gateway': gateway_name,
        'type': gateway_type,
        'api': _set_api(),
        'whitelist': _set_white_list(),
        'callback_url': CALLBACK_URLS[f'{gateway_type}'],
        '_force_https': False,
        'note': '',
        'expires': 15,
        'decimals': 2,
        'random_decimals': 0,
        'currency': _set_currency(),
        'pay_type': 0,
        'pay_method': 0,
        'user_rating': 0,
        'amount_type': 0,
        'amount_min': 1,
        'amount_max': 999999999,
        'amount_fixed': [50, 100, 200],
        'payer_cred': {},
        'extra': {},
    }
    return data


def _set_type(retry=False) -> int:
    """設置三方類型"""
    _PAY = 0
    _TRANSFER = 1
    if not retry:
        print('說明：設置第三方類型(填入數字)[1=支付, 2=代付]')
    gateway_type: int = try_input_int('設置：')
    if gateway_type not in [1, 2]:
        print(f'{gateway_type} 在清單中沒有對應的值，請重新輸入。')
        return _set_type(retry=True)
    return _PAY if gateway_type == 1 else _TRANSFER


def _set_api(retry=False) -> str:
    """設置api"""
    if not retry:
        print('說明：下單網關[支付填寫HOST+API|代付填寫HOST]')
    api: str = input('設置：')
    if not re.match(API_PATTERN, api):
        print(f'地址 {api} 不符合http協議規格，請重新填寫。')
        return _set_api(retry=True)
    return api


def _set_white_list(retry=False) -> List[str]:
    """設置ip"""
    if not retry:
        print('說明：回調IP白名單, IP之間以,做為分隔。Ex:a, b, c, d')
    ips: List[str] = str_to_list(input('設置：'))
    for ip in ips:
        if not re.match(IP_PATTERN, ip.replace('.', '')):
            print(f'IP {ip} 不符合ip規格，請重新輸入。')
            return _set_white_list(retry=True)
    return ips


def _set_currency(retry=False) -> str:
    """設置貨幣"""
    if not retry:
        print('說明：設置交易貨幣類型(填入數字)[1=RMB, 2=USDT_ERC20, 3=USDT_TRC20]')
    code: int = try_input_int("設置：")
    currency: str = f'{code - 1}'
    if currency not in CURRENCIES.keys():
        print(f'{code} 在清單中沒有對應的值，請重新輸入。')
        return _set_currency(retry=True)
    return CURRENCIES[currency]
