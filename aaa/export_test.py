import inspect


def r():
    result = []
    d = {0: 0, 1: 1, 2: 2, 3: 3, 4: 4}
    for i in range(4):
        # # 原版測試
        # return [lambda x: x * i for i in range(4)]

        # if else測試
        # if i == 0:
        #     result.append(lambda x: x * 0)
        # elif i == 1:
        #     result.append(lambda x: x * 1)
        # elif i == 2:
        #     result.append(lambda x: x * 2)
        # elif i == 3:
        #     result.append(lambda x: x * 3)

        # get測試
        y = d.get(i)
        result.append(lambda x: x * y)
    return result


class O:
    def __init__(self):
        self.name = 'kevin'


if __name__ == '__main__':
    o = O()
    a = o
    a.name = 'jojo'
    print(o.name)
    print(a.name)
    # ans = r()
    # # print(ans)
    # print([inspect.getsource(m) for m in ans])
a = {
    "alias": "爆炸支付支付宝H5",
    "amount_fixed": "50,100,200",
    "amount_list": "",
    "amount_max": "5000.00",
    "amount_min": "10.00",
    "amount_recommend": "",
    "amount_type": "free",
    "channel_extra": "{\"urlskip\": \"True\"}",
    "evaluation_list": "",
    "extra": "{\"payType\": 103}",
    "fee_ratio": "0.00",
    "fee_type": "2",
    "gateway_id": "7",
    "grants": "1.00",
    "img": "https://apimg.alipay.com/combo.png?d=cashier&t=alipay",
    "name": "爆炸支付支付宝H5",
    "online": true,
    "pay_method": "alipay",
    "pay_type": "alipay",
    "payee_method": "redirect",
    "plat_enable": {},
    "rating": "1",
    "scope": "",
    "svip": false,
    "vip_list": "0,0.5,1,2,3,4,5,6",
    "w": "0"
}