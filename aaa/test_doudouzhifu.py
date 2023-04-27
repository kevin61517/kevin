# flake8: noqa

import pytest
from sanic import Request
from payment.gateway import RequestDecoder
from payment.encoder import Encoder, CONTENT_TYPES
from payment.gateway.doudouzhifu import PayCallbackData, PayCallbackDecoder, PayRequestData, PayResponse, Signer
from payment.helpers import json_dumps, to_bytes, asdict
from payment.httpclient.models import HTTPResponse
from tests.factories import GatewayConfigFactory, OrderFactory

# 網關資料
APP_ID = '2952e7454cfc4143'
APP_SECRET = '7fdb56f490644a9f8511f8a2c6198ebc'
CALLBACK_URL = "https://71a0-18-163-217-66.ap.ngrok.io/api/payment/callback/DouDouZhiFu"
EXTRA = {"paymode": "BANK_CARD"}
API = 'https://api.doudoupays.com/gateway/pay/deposit'

# 訂單資料
ORDER_NO = '1111111115'
AMOUNT = "50100"

# 簽名資料
SOURCE = '{"mchCode":"2952e7454cfc4143","orderId":"1111111115","amount":501,"paymode":"BANK_CARD","notifyUrl":"https://71a0-18-163-217-66.ap.ngrok.io/api/payment/callback/DouDouZhiFu"}7fdb56f490644a9f8511f8a2c6198ebc'  # 下單的簽名資源
SIGN = 'cd4cd9a3c5b6234f136c096d4e2196e9'  # 下單的簽名
SPEC_COLUMN = {}  # 設置會影響簽名的唯一值類型參數 Ex: timestamp，用法：key=參數名稱 value=參數值 -> {'payTime': '1234567890'}
SIGN_COLUMN = 'sign'  # 簽名參數的名稱 Ex: 'md5_sign'

# 回調資料
CALLBACK_TYPE = "FORM".upper()  # 回調方式FORM, JSON
CALLBACK_AMOUNT = 501
CALLBACK_ORDER_NO = '1111111115'
CALLBACK_TRANS_NO = ''


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
                {'retcode': 0, 'retdesc': 'success', 'data': None, 'qrcodeUrl': None,
                 'payUrl': 'https://otc.lvdoupay.top/?billId=644005e158459e0da8595c75', 'amount': 501, 'payAmount': 501,
                 'success': True},
                {"exc": None, }
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
        assert cred.url == ""
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
                {'amount': '501', 'payAmount': '501', 'orderId': '1111111115',
                 'sign': '25b7eeab45edb8f72b57274ab7900d5e', 'completeTime': '20230419232958', 'status': '0'},
                {
                    "exc": None,
                    "paid": True,
                    "amount_paid": int(CALLBACK_AMOUNT),
                    "order_no": CALLBACK_ORDER_NO,
                    "trans_no": CALLBACK_TRANS_NO,
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
        url_bytes=to_bytes(f"/api/payment/callback/DouDouZhiFu"),
        headers={"content-type": CONTENT_TYPES.get(CALLBACK_TYPE, "")},
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
