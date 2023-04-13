from .tools import str_to_list, try_input_char
from payment.constants import ALGOS, PRESIGN_STR


def set_signer():
    print('== 設置簽名器 == ')
    data = {
        'excludes': _excludes(),
        'algo': _algo(),
        'salt': "&key={cfg.appsecret}",
        'presign': '"&".join([f"{k}={v}" for k, v in self.iter_fields(data) if v]) + f"&key={self.cfg.appsecret}"',
    }
    return data


def _excludes() -> list:
    """設置不參與簽名的字段"""
    print('== 設置不參與簽名的字段 ==')
    print('說明：字段之間以,做為分隔。Ex:a, b, c, d')
    s: str = input('設置：')
    result = str_to_list(s)
    print('設置的排除字段為', result)
    return result


def _algo(retry=False) -> str:
    """設置加密算法"""
    if not retry:
        print('== 設置加密演算法 ==')
        print('說明：輸入加密演算法名稱')
        print('支援清單')
        print(' | '.join([f'{k}={v}' for k, v in ALGOS.items()]))
    algo = try_input_char('設置：')
    if algo not in ALGOS.keys():
        print(f'{algo}在清單中沒有對應的值，請重新輸入')
        return _algo(retry=True)
    algorithm = ALGOS[algo]
    print(f'選擇的加密算法為：{algorithm}')
    return algorithm


# TODO 尚未完成
def _salt():
    """設置鹽"""
    ...


# TODO 尚未完成
def _presign():
    """設置簽名前期字串"""
    print('== 設置加密前期字串拼接 ==')
    print('說明：加密字串的拼接方式 Ex: key1=value1&key2=value2')
    sort = input('是否按照昇序排列[y|n]')
    if sort == 'y':
        print('== 昇序排列 ==')
        print('支援的拼接方式：')
        print('\n'.join(f'{k}={v}' for k, v in PRESIGN_STR.items()))
    else:
        print('== 自定義排列 ==')


d = {
    'gateway': ['測試付'],
    'type': ['0'],
    'api': ['http://testfu/api'],
    'callback_url': ['{host}/api/payment/transfer/callback/{gateway}'],
    '_force_https': ['False'],
    'whitelist': ['11.22.3.4, 123.456.7.8'],
    'expires': ['15'],
    'decimals': ['2'],
    'random_decimals': ['0'],
    'currency': ['RMB'],
    'pay_type': ['0'],
    'pay_method': ['0'],
    'user_rating': ['0'],
    'amount_type': ['0'],
    'amount_min': ['1'],
    'amount_max': ['999999999'],
    'amount_fixed': ['100, 200, 300'],
    'payer_cred': ['{}'],
    'extra': ['{}', '{}'],
    'algo': ['md5'],
    'excludes': ['sign, remark'],
    'salt': ['加鹽測試'],
    'presign': ['"&".join([f"{k}={v}" for k, v in self.iter_fields(data)]) + self.salt(data)'],
    'RequestMethod': ['POST+JSON'],
    'req_data_key': ['mchId', 'orderId', 'amount', 'notifyUrl'],
    'req_data_valuer': ['cfg.appid', 'order.order_no', 'order.amount', 'cfg.callback_url'],
    'req_signer_key': ['sign'],
    'req_signer_valuer': ['sign'],
    'rsp_data_key': ['payUrl'],
    'rsp_data_valuer': ['ppp'],
    'mapper_data_key': ['url'],
    'mapper_data_valuer': ['self.payUrl'],
    'CallbackParser': ['request.json'],
    'cal_data_key': ['mchId', 'orderId', 'amount'],
    'cal_data_valuer': ['mmm', 'ooo', 'aaa'],
    'cal_signer_key': ['sign'],
    'cal_signer_valuer': ['sign'],
    'CallbackResponse': ['success'],
    'merchants_name': ['t001'],
    'display_name': ['0-100'],
    'appid': ['001'],
    'appsecret': ['abcd1234'],
    '_tenants': ['tyc']
}

# 網關資料
APP_ID = '20211216'
APP_SECRET = 'reTbuqLzSJGQtPvjBkgnifsRaNZhxAUD'
CALLBACK_URL = 'http://9c51-18-166-200-86.ngrok.io/api/payment/callback/YiXiangBaoZhiFu'
EXTRA = {
    "channel": "zfbsm",
    "r_pri_key": "MIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQCpaLnsb2ffIPSgiEMjEdNzwIvRVv/1mWrbVJFOup9ZmlpEgw1tW1A/KDqIE1ND5sphgw7tz/HjFAZreJHafVmTd6L7A4u+dU6wwCr/VIHzJ/SENw21p+kjiGxcaQVExHFCE/95orEa/zfWyRGMdSaoNXRRlFsCTGCyQ655dtfk4MGQYYeyBZnsPswMRqQ1DtT6mPPf5ta7JrhckK0awTHc0ofFZHCi0sa/K017RlNf4Oyq9FuwRCCQkDdwYq5LopnSGBREROCwPeJ5pUCdu+sHg0UP0DQX9aXxZIHDPYqEuboLbHZnfNpcXmaqs8aVudTlDWjvCjjpe0lFg3G9pFl9AgMBAAECggEBAJkLOVv10TrshNM6Bpz6D7M0sZtvI1F3RefbYGJlimviW8YlNs4ifj5wU2B3RPPE3fR199iz0Ww5vQr+I5XlRDVLEXv/WhG33F0lXjLI35UR9X40VjhT9vTY3DwnzFCxvzfY5SW36pPfGUz63NWtSD0R/YFtq0JKSdkB9+9Xg/cJ9M0bXpqeAaCue7gheEDDB4wuW1wV1Aw7PCHJkIABSTM9Lf8W89JRRX0Q4640vuBk248d/CLxvKAbbhNZ3pijRwvEX799dpWVyCQ5OR0OezjeF+7wXEAV1veDnLsCy/bHWHEXSJN/QrwxyqmYgXHdTKnJDLstcKMBV5tajjK3TSkCgYEA0TaLK+tk8/tBQRmzGpeCutyuqfeYpeq/8lIRcpAMUyzQ1lFVM6YzJtZQvDEF06Mi+yjNSFhyLq+D9Cu6Qmoaf36onltkO/h1VNNoFu44m4iH1KnZiYbMzXxPvsUOKdIHRTvD2DP4Pzihi3bN3Xdxdk7GttQwA7gsU2Nple+JsCsCgYEAz0tnSariAcuHHBs93Mew42fjflh6rJtOp0SPN5hEZEjhWpOg4UwyE1R3C7Y555nJ8CRlPS1Mrz1y+LiU3nhtW0z+zKxhkGiNCmBMaWazUCf0NvbHIgrv5TlosicrPWiHNBkWjMXJgHatHRWH3JGbLaLMo4qC/LZLQa/C+fRSIPcCgYA9c5n5cpEaoSiPqK7VFr/Nh1i+j/2Ebqmm0bhSQEF+hOFqskUmgKDxvW3FeVjOy1JRF7EEmQYg9Gj75YQ2Udgqrtd0fD+65cYA/n/KjHqQJNBRBPrizHeHvAXocRUx74E3MtDZxpoaZ9X7kw/xB06Kg6UWusjHrudGLyMqaUu2NQKBgFV4k7fuO43d63GNUe6Mb8Tz+vsHZF1zE/Un8Z1MrTZkTnbYVAdRMXyC4Sr1Ed8KrBbWCuA0o1/GCHfBM7CfGwgAMTcXBItUcIMMvbTf4aN1Nd7L1cOVmuB60U5TlCKXzNeQWJnmm3Taefp5/DDX4JHqhFISNHwadeE5pT0Gni51AoGAYtm8uKerKFKXLk5QGrJPkeib80kiMLJYbUcGiVyuc6ZDS1lZkAQIaY5uZazwGzZpAkd375HuxblmxqhGJbt2YQkcmdAQ7G0ggNpLUmcFS2n+3QF72IiJPfKHHu4JwCNDHTqVt0NOld4b/yQKONbdsBW6AS/yt7f9sXDQSK69HcQ=",
    "r_pub_key": "MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEArWFCS5PDULTl+loYyOMhh5kYEqlFmQbq+R39tsRggoynUuamQx9WhWzgcUAr/mGFrp/10beUpcVvyh9o6mPZz33cOg4wYJkM4yXRhvn+uxiVkM2UOMpDlUd1wB4sqMWs62uiOBwRaHpR9NuWyL9+/9uNJn6W+btaQLsSjCt6SgBnFwhcwa5iWJ0Xlsk1DfWDeeleUD8dRN+CbVTsTqBmC9dEaoBXYkIJk3AK/VyVuxktgvOrHYyE/eZd9lHEnDxphrWnUCG4xqJzSXxLusKr2c9628AhoLhLbHeZ7HG7e3Z+LYeKxmcP6TdDtBk2AMMAYjR5gFVRVdoPpF7PuvaDwwIDAQAB"
}
API = 'http://api.yxblianmeng4z.com/api/pay'

# 訂單資料
ORDER_NO = '1234567895'
AMOUNT = 200000

# 簽名資料
SOURCE = 'channel=zfbsm&desc=-&ip=18.166.200.86&merId=20211216&nonceStr=514qe7ysPfYnvbIU&notifyUrl=http://9c51-18-166-200-86.ngrok.io/api/payment/callback/YiXiangBaoZhiFu&orderAmt=2000&orderId=1234567895&returnUrl=http://9c51-18-166-200-86.ngrok.io/api/payment/callback/YiXiangBaoZhiFu&key=reTbuqLzSJGQtPvjBkgnifsRaNZhxAUD'
SIGN = 'iOoivKei5lqtSuxwN/STzbUD/PNLdP8mP68jpwI0R8gx4zpHt4/TCnc44RJxdCVDcHCSBTqEwP1M5KaYqhKWjMC3f5osp1G4yQOmK4hUuieQEbH2KVpiCzmb2LBGvQBsDG8w3VtckFuVwFt5farr3Y4mmcDuiAfVBhoUbK6rw1wchqwQkowMIc7xFq1ibeSnpb+cWbXfNZ3kQ+mKXDevFvzlF4a74dSPXbzYXDIMUj2scANoyLzbAwJznl7Jdb/SIHwWzZyBrhxB7v2212PZ4h7yBYKSy64Ik0eomHsclL5zQgGLaH90tCOxwYTa+KZJn6seLbz1s33ATBriYmTzig=='
SPEC_COLUMN = {
    'nonceStr': '514qe7ysPfYnvbIU',
    'ip': '18.166.200.86'
}  # 設置會影響簽名的唯一值類型參數 Ex: timestamp，用法：key=參數名稱 value=參數值 -> {'payTime': '1234567890'}
SIGN_COLUMN = 'sign'  # 簽名參數的名稱 Ex: 'md5_sign'

# 回調資料
CALLBACK_TYPE = 'FORM'  # 回調方式FORM, JSON
TRANS_NO = '1638945979926993219'  # 第三方平台訂單號


