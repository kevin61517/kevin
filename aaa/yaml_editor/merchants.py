from .tools import List, try_input_int


def merchants_edit(gateway_name: str, gateway_type: int) -> List[dict]:
    # 編輯商戶資料
    merchants: List[dict] = _set_merchants(prompt_message='設置商戶資料')
    # 編輯渠道資料
    channels: List[dict] = _set_channels(gateway_type=gateway_type, prompt_message='設置渠道資料')
    # 三方類型[0=支付|1=代付]
    gateway_is_pay = f'{gateway_type}' == '0'
    result = []
    for channel in channels:
        v = channel.pop('v', '')  # extra的值
        for mch in merchants:
            name = f'{gateway_name}-{v}-{mch["appid"]}' if gateway_is_pay else f'{gateway_name}-{mch["appid"]}'
            channel['name'] = name
            # 容器物件必須deep copy，否則yaml上的值會變成指標...
            if channel.get('extra'):
                channel['extra'] = {**channel['extra']}
            mch['_tenants'] = [e for e in mch['_tenants']]
            result.append({**mch, **channel})
    return result


def _set_merchants(prompt_message='') -> List[dict]:
    """配置支付商戶"""
    print(f'== {prompt_message} ==')
    result = []
    n = try_input_int('請輸入商戶數量：')
    for _ in range(1, n+1):
        print(f'== 第 {_} 組商戶配置 ==')
        result.append({
            'appid': input('設置商戶號：'),
            'appsecret': input('設置商戶密鑰：'),
            '_tenants': input('支持的平台，用,分隔 Ex: vns8, tyc：').replace(' ', '').split(','),
        })
    return result


def _set_channels(gateway_type, prompt_message='') -> List[dict]:
    """配置渠道"""
    print(f'== {prompt_message} ==')
    f_map = {
        'str': str,
        'int': int,
        'float': float
    }
    result = []
    channel_key = None
    channel_format = None
    if f'{gateway_type}' == '0':
        n = try_input_int('請輸入渠道數量：')
        for _ in range(1, n + 1):
            print(f'== 第 {_} 條渠道配置 ==')
            """支付渠道"""
            if channel_key is None:
                channel_args = input('請輸入渠道編碼鍵, 編碼值, 編碼資料型態，以,分隔。Ex: trade_type, 1, str：').replace(' ', '').split(',')
                channel_key = channel_args[0]
                channel_format = f_map.get(channel_args[-1], str)
                code = channel_format(channel_args[1])
            else:
                channel_args = input(f'渠道編碼鍵為{channel_key}，請輸入渠道編碼值：')
                code = channel_format(channel_args)
            result.append({
                'display_name': '0-100',
                'pay_type': _set_pay_type(),
                'extra': {channel_key: code, **_set_extra()},
                'v': code  # 渠道編碼
            })
    else:
        """代付渠道"""
        result.append({'display_name': '0-100', 'extra': _set_extra()})
    return result


def _set_extra() -> dict:
    print('== 設置渠道額外參數 ==')
    result = {}
    if input('是否需要填寫渠道額外參數？[y|n]').lower() == 'y':
        while True:
            key = input('設置渠道額外參數key：')
            value = input('設置渠道額外參數value：')
            result[key] = value
            keep = input('是否繼續？[y|n]')
            if keep.lower() == 'n':
                break
    return result


def _set_pay_type(retry=False):
    if not retry:
        print('== 設置渠道類型[1=微信, 2=支付宝, 3=银联转账, 4=银行卡, 5=加密货币] ==')
    v = input('請輸入數字: ')
    _map = {
        '1': 0,
        '2': 1,
        '3': 2,
        '4': 3,
        '5': 4,
    }
    if v and v not in _map.keys():
        print(f'{v}在清單中沒有對應的值，請重新輸入。')
        return _set_pay_type(retry=True)
    return _map[v]
