import requests
import json
import hashlib
from ciphers import cipher
from decimal import Decimal


class Signer:
    def __init__(self, key):
        self.key = key

    def _pre_sign(self, data: dict) -> str:
        """簽名前處理"""
        source = '&'.join((f'{k}={v}' for k, v in sorted(data.items()) if v))
        print('簽名資源：', source)
        return source

    @staticmethod
    def _sign(source: str) -> str:
        """簽名"""
        m = hashlib.md5(source.encode("utf8"))
        return m.hexdigest()

    @staticmethod
    def _post_sign(sign: str) -> str:
        """簽名後處理"""
        return sign

    def exec(self, data: dict):
        """執行簽名"""
        source = self._pre_sign(data)
        sign = self._sign(source)
        return self._post_sign(sign)


class Payment:
    def __init__(self, mch_id, url, key):
        self.mch_id = mch_id
        self.url = url
        self.signer = Signer(key)

    def pay(self, payload):
        """下單
        {
            'retcode': 0,
            'retdesc': 'success',
            'data': None,
            'qrcodeUrl': None,
            'payUrl': 'https://otc.lvdoupay.top/?billId=643ff99e58459e0da8592453&repeat=1',
            'amount': 500,
            'payAmount': 500,
            'success': True
        }
        """
        order_no = payload.get('orderno')
        amount = payload.get('amount')
        pay_type = payload.get('code') or 'ALIPAY_QR'
        data = {
            'mno': self.mch_id,
            'orderno': order_no,
            'amount': Decimal(amount) * 100,
            'code': pay_type,
            'async_notify_url': 'http://89e6-18-163-217-66.ngrok.io/test/notify'
        }
        sign = self.signer.exec(data)
        data['sign'] = sign
        resp = requests.post(self.url, json=data)
        data = self._parse_resp(resp)
        final = self._verify_pay(data)
        return {'payUrl': final.get('payUrl')}

    @staticmethod
    def _parse_resp(resp):
        """解析返回"""
        data = resp.json()
        return data

    @staticmethod
    def _verify_pay(data):
        """驗證"""
        if data.get('retcode') == 0:
            return data
        return {'msg': '下單資料驗證錯誤', 'status': 400, 'data': data}

    def notify(self, data):
        """回調
        {
            'amount': '500',
            'payAmount': '500',
            'orderId': '1234567899',
            'sign': 'a6fc08d37be99d128ab9b41867aa71ac',
            'completeTime': '20230419223145',
            'status': '0'
        }
        """
        data['mchCode'] = self.mch_id
        payload = self._verify_notify(data)
        if self._verify_sign(payload):
            return payload
        return {'msg': '簽名驗證失敗。', 'data': data}

    @staticmethod
    def _verify_notify(data):
        """驗證回調資料"""
        if data.get('status') == '0':
            return data
        return {'msg': '回調驗證失敗', 'status': 400}

    def _verify_sign(self, data) -> bool:
        """驗證回調簽名"""
        _3rd_sign = data.get('sign')
        _our_sign = self.signer.exec(data)
        data.pop('mchCode', '')
        return _3rd_sign == _our_sign

