import requests

"""
TransferRequestData(mchid='10052', out_trade_no='1234567899', money='1.00', bankname='中国建设银行', subbranch='台銀', accountname='大老爸', cardnumber='5149588888888887', province='江苏省', city='北京', paypassword=None, notifyurl='http://0.0.0.0:5001/api/payment/transfer/callback/NaiSiDaiFu', pay_md5sign='F8DAEE24D082F68F1B5500BFBF172EEE')
"""
url = 'https://dipayway.cc/Payment_Dfpay_add.html'
# data = {
#     'mchid': '10052',
#     'out_trade_no': '1234567899',
#     'money': '100',
#     'bankname': '中国建设银行',
#     'subbranch': '台銀',
#     'accountname': '大老爸',
#     'cardnumber': '5149588888888887',
#     'province': '江苏省',
#     'city': '北京',
#     'notifyurl': 'http://0.0.0.0:5001/api/payment/transfer/callback/NaiSiDaiFu',
#     'pay_md5sign': 'F8DAEE24D082F68F1B5500BFBF172EEE'
# }


def factory():
    yield from (f'產品{n}' for n in range(1, 4))


def consumer():
    while True:
        data = yield
        print(f'客戶使用商品--->{data}')


if __name__ == '__main__':
    fac = factory()
    con = consumer()
    next(con)
    for product in fac:
        con.send(product)
