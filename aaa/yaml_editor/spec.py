from .signer import set_signer as _set_signer
from .tools import Union, List, try_input_int


def spec_edit(gateway_type) -> dict:
    gateway_is_transfer = f'{gateway_type}' == '1'
    title = 'Transfer' if gateway_is_transfer else 'Pay'
    data = {
        'Signer': _set_signer(),
        f'{title}RequestMethod': _set_request_method(),
        f'{title}RequestData': _set_arguments('下單參數', init_sign=False),
        f'{title}Response': _set_arguments('下單返回參數'),
        f'{title}CallbackParser': _set_callback_parser(),
        f'{title}CallbackData': _set_arguments('回調參數'),
        f'{title}CallbackResponse': _set_value('回調響應 Ex: success')
    }
    if gateway_is_transfer:
        data.update(
            {
                'TransferApi': _set_value('下單API'),
                'QueryTransferRequestData': _set_arguments('查單參數', init_sign=False),
                'QueryTransferApi': _set_value('查單API'),
                'QueryTransferResponse': _set_arguments('查單返回參數')
            }
        )
    return data


def _set_value(prompt_message='', converter=lambda v: v) -> Union[str, int]:
    """
    設置單一參數
    prompt_message: 提示訊息
    converter: 轉換器
    """
    print(f'== 設置{prompt_message} ==')
    return converter(input(f'設置: '))


def _set_arguments(prompt_message='', init_sign=True) -> List[dict]:
    """
    設置多個參數
    prompt_message: 提示訊息
    init_sign: 實例化簽名
    """
    print(f'== 設置{prompt_message} ==')
    print('說明: 參數之間以,作為間隔，存放簽名值的字段以!!作為開頭。Ex:a, b, c, d, !!sign')
    s: str = input(f'輸入參數：')
    result = []
    for element in s.replace(' ', '').split(','):
        if element.startswith('!!'):
            result.append({'field': element[2:], 'type': 'SignField', 'init': init_sign})
        else:
            result.append({'field': element})
    return result


# TODO
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
    print('1.先輸入所需參數數量\n', '2.用 = 來表示參數對應值。\n', '3.用 = 來表示參數的類型[i=整數, f=浮點數, s=字串, d=Decimal]。', sep='')
    print('完整範例：', 'amount=order.amount=i\n', 'timestamp=timeP=YYYY-MM-DD hh-mm-ss-ff', sep='')
    n: int = try_input_int('參數數量：')
    result = []
    for i in range(1, n+1):
        f, v, fmt = 0, 1, 2
        data = input(f'設置第 {i} 個參數：').split('=')  # data = 'key=value=format'
        field, value, format_ = data[f], data[v], f_map[data[fmt]]
        if value.startswith('!!'):
            result.append({'field': field, 'type': 'SignField', 'init': init_sign})
        elif value == 'timeP':
            result.append({'field': field, 'valuer': f'TimeStamp.timestamp_custom({format_})'})
        elif value == 'timeU':
            result.append({'field': field, 'valuer': f'TimeStamp.timestamp_digit({format_})'})
        else:
            result.append({'field': field, 'valuer': f'{format_}({value})'})
    return result


def _set_request_method(retry=False) -> str:
    """
    設置發請求的資料傳輸格式
    json, form, text
    """
    if not retry:
        print(f'== 設置發請求的資料格式[1=JSON, 2=FORM, 3=TEXT] ==')
    v = input('請輸入數字: ')
    _map = {
        '1': 'JSON',
        '2': 'FORM',
        '3': 'TEXT'
    }
    if v and v not in _map.keys():
        print(f'{v} 在清單中沒有對應的值，請重新輸入。')
        return _set_request_method(retry=True)
    return 'POST+' + _map.get(v, 'FORM')


def _set_callback_parser(retry=False):
    """
    設置三方回調的請求方式
    json, form, args
    """
    if not retry:
        print(f'== 設置回調解析[1=JSON, 2=FORM, 3=ARGS] ==')
    v = input('請輸入數字: ')
    _map = {
        '1': 'json',
        '2': 'form',
        '3': 'args'
    }
    if v and v not in _map.keys():
        print(f'{v}在清單中沒有對應的值，請重新輸入。')
        return _set_callback_parser(retry=True)
    return 'request.' + _map.get(v, 'form')
