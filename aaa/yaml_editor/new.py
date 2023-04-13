# flake8: noqa
import pytest
from sanic import Request

from payment.exceptions import (
    ChannelParseError,
    ChannelRespCodeError,
    ChannelUnexpectedError,
)
from payment.gateway import RequestDecoder
from payment.typed import SignField
from payment.encoder import Encoder
from payment.gateway.yixiangbaozhifu import (
    PayCallbackData,
    PayCallbackDecoder,
    PayCallbackEncoder,
    PayRequestData,
    PayResponse,
    Signer,
)
from payment.helpers import json_dumps, to_bytes, asdict
from payment.httpclient.models import HTTPResponse
from tests.factories import GatewayConfigFactory, OrderFactory
from payment.typed import Nil, SignField


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


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "data, result",
    [
        (
            {
               "amount": AMOUNT,
               "order_no": ORDER_NO,
            },
            {
                "digest": SIGN,
                "source": SOURCE,
            },
        )
    ],
)
async def test_Signer(data, result):
    cfg = GatewayConfigFactory.build(
        appsecret=APP_SECRET,
        appid=APP_ID,
        callback_url=CALLBACK_URL,
        extra=EXTRA,
        api=API,
    )
    order = OrderFactory.build(cfg=cfg, **data)
    req = PayRequestData.create(order)
    for k, v in SPEC_COLUMN.items():
        setattr(req, k, v)
    signer = Signer(cfg)
    assert signer.presign(req) == result["source"]
    assert signer.sign(req) == result["digest"]


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "data, result",
    [
        (
            {
               "amount": AMOUNT,
               "order_no": ORDER_NO,
            },
            {
                "digest": SIGN,
                "source": SOURCE,
            },
        )
    ],
)
async def test_PayRequestData(data, result):
    cfg = GatewayConfigFactory.build(
        appsecret=APP_SECRET,
        appid=APP_ID,
        callback_url=CALLBACK_URL,
        extra=EXTRA,
        api=API,
    )
    order = OrderFactory.build(cfg=cfg, **data)
    req = PayRequestData.create(order)
    for k, v in SPEC_COLUMN.items():
        setattr(req, k, v)
    signer = Signer(cfg)
    assert req.make_sign(signer) == result["digest"]
    assert getattr(req, SIGN_COLUMN) == result["digest"]
    for k, v in asdict(req).items():
        assert getattr(req, k) == v


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "data, result",
    [
        (
            {
                'code': 1,
                'msg': '请求成功!',
                'time': '1638945979',
                'data': {
                    'payurl': 'http://8.210.255.135/f007c7614c158feaae30ba36daa5fe6648613cd3badd5f1c9c881aa51d93ca0116389459790742bb590454e6f89659f1373714c550',
                    'orderno': '1234567895',
                    'sysorderno': '1638945979926993219'
                }
            },
            {
                "exc": None,
            },
        ),
    ],
)
async def test_PayResponse(data, result):
    cfg = GatewayConfigFactory.build(
        appsecret=APP_SECRET,
        appid=APP_ID,
        callback_url=CALLBACK_URL,
        extra=EXTRA,
        api=API,
    )
    resp = HTTPResponse(
        content=to_bytes(json_dumps(data)),
        url=cfg.api,
        request_info=None,
    )

    def t():
        dec = PayResponse.create(resp)
        dec.verify()
        cred = dec.decode()
        assert cred.url == data['data']['payurl']
        assert cred.type

    if result["exc"]:
        with pytest.raises(result["exc"]):
            t()
    else:
        t()


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "data, result",
    [
        (
            {
                "merId": "20211216",
                "orderId": "1234567895",
                "sysOrderId": "1638945979926993219",
                "desc": "-",
                "orderAmt": "2000.00",
                "status": "1",
                "nonceStr": "WcqZk078QOh1pns3flErtF6IoJjLVwiD",
                "sign": "MNJ0bcLZT00QcgQcTnARJQ8PQu9ja4jin0MqSTZFzg8reBqsVF5okpGhb5CEilpY7u26gvAzV4Q8QEfRihslR7eAnDcDqTv05xg10y1Terancq8xVvhLzJoTzWwsVYEHQysdwn9TLXB1vDOMLfgiJf+P8YCuVIklxxKCo/fyAP/dbOTneXNPaExx0GHAJ/0kE+Vnppz8qccwM3m1giWorR1X1UeWmfmQPSHFfkSSn9gGQj44Win/tC32W2NosrTKhGyppbJvdIjTysem10doJNgMYPh6YzOMyC6Bhu/zJ7Noj1VHUdbrsqtkxaxKnjuMjoGtsrv9NnRj79PsMxOhgA==",
            },
            {
                "exc": None,
                "paid": True,
                "amount_paid": int(AMOUNT),
                "order_no": ORDER_NO,
                "trans_no": TRANS_NO,
            },
        ),
    ],
)
async def test_CallbackDecoder(data, result):
    cfg = GatewayConfigFactory.build(
        appsecret=APP_SECRET,
        appid=APP_ID,
        callback_url=CALLBACK_URL,
        extra=EXTRA,
        api=API,
    )
    order = OrderFactory.build(
        notify_url="https://mockcb.com/cbtest/fff", amount=100032
    )

    req = Request(
        method="POST",
        url_bytes=to_bytes(f"/api/payment/callback/YiXiangBaoZhiFu"),
        headers={"content-type":"application/x-www-form-urlencoded"},
        version="",
        transport=None,
        app=None,
    )
    # req.body = JSONEncoder().encode(data)
    req.body = Encoder.make(CALLBACK_TYPE)().encode(data)

    signer = Signer(cfg)
    dec: RequestDecoder = PayCallbackDecoder.create(req)
    dec.verify(signer)
    cb: PayCallbackData = dec.decode()
    dec.verify_sign(signer=signer, req=req)  # 測試驗籤
    assert cb.paid == result["paid"]
    assert cb.amount_paid == result["amount_paid"]
    assert cb.order_no == result["order_no"]
    if result.get('trans_no'):
        assert cb.trans_no == result["trans_no"]

appid = '10619'
key = 't41j5aeu8ppt2549nivggrf4534gg10g'
extra = {"aes_key":"mndRGqYJz7bEgbUX5d349FbPZpCAqmAalfiTKrzIBHpS3xNaDolOmIy7HSDRje7O"}  # 10619
extra2 = {"aes_key":"b8xtSPEKxcoAWv1Jwndd5Fray1fIY3rgr5KmczRjSBHTdHX5mXURDbxppbe4BqHm"}  # 10657

fff = 1
