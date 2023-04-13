from typing import List, Dict, AnyStr


CALLBACK_URLS = {
    '0': "{host}/api/payment/callback/{gateway}",  # 0=支付
    '1': '{host}/api/payment/transfer/callback/{gateway}',  # 1=代付
}


data = {
    'gateway': str,
    'type': int,  # 0=支付, 1=代付
    'api': str,  # http://123.456.7.8
    'whitelist': List[str],
    'callback_url': CALLBACK_URLS[f'{1}'],  # 回調地址
    '_force_https': False,
    'note': '',
    'expires': 15,
    'decimals': 2,
    'random_decimals': 0,
    'currency': str,  # RMB, USDT_ERC20, USDT_TRC20
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


def spec_edit(gateway_type) -> dict:
    gateway_is_transfer = f'{gateway_type}' == '1'
    title = 'Transfer' if gateway_is_transfer else 'Pay'
    data = {
        'Signer': Dict,  # {'excludes': List[str], 'algo': str}
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