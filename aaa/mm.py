import hashlib
import requests
import json
import base64
from ciphers import cipher, Message, BaseCipher
import Cryptodome.Signature.PKCS1_v1_5 as sign_PKCS1_v1_5
import Cryptodome.Cipher.PKCS1_v1_5 as Cipher_pkcs1_v1_5
from decimal import Decimal
from Cryptodome.PublicKey import RSA
from Cryptodome.Hash import SHA256
from php_test import php
import subprocess


class Demo:
    """"""
    def __init__(self):
        # 測試下單
        self.mch_id = 'A16'
        self.md5_key = 'c6d1d0dbc0394476be95a47851151581'
        self.token = '48692ade-e76f-4a1e-9a86-af4e7c8bd84a'
        self.rsa_pub_key = 'MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCinWLwAHERO8tBVfTHdkZIOF7VSKQr04auwTR39MruGtqXbmvbzTd5omLm6wNbEc3X9mJ1x2ckbR/RQVp0plG6swZLFvSzo7XW6X9spAM4kC+8nj/tqF7cSET8wEwQ3gcEpC2R1vfFkM/iQtyu6CJbxccsuPGiqAKJOiYOl+qMUwIDAQAB'
        self.rsa_pri_key = 'MIICdwIBADANBgkqhkiG9w0BAQEFAASCAmEwggJdAgEAAoGBAPb5gvFOV95Umh6+AqEwyugfJch/O/rP7FVLDDiQEA0/62KK4ej1zxBx9tKGhYE87C3ba0hAiajew5YnJN73prVv2stYqwH0GkKU6C1VZF5+VI+lfX8JcCU3SLrYtCrRQ9IIJX5K35hDZmKvriFmiaI2yrZ7ATZbv1QwmWBhB/PbAgMBAAECgYEA6plWjbs6ckHw6FTbkJwVkerMbCiYJAZP2zFfmXcXGE7oXAHK2AxutZNbvtzzgjEJtAGiZc6QNO3t4fqq5nVeT0sKoxSp530a0kicdW9rJAeWU69Pt4Pt2dpWh0TIwZM40V4Tmk2MpD746MYc0ONuDS+hvvA5MT+n0O5JuYvQkFECQQD9c3MGhz/dPe1OlW9B1B08gRyHQjWLtRrstODMrccwBtChfsgZgSpJ70IB64oi1lco7LDavsP2uyAYdvU664CDAkEA+XVjSXibChDxk1OAyKgOBhHC8lTnKyz4lUurx1vFN7/MHWdm6o5d8DMmKQjm814mjQ87H1cFymhngVXiUdgvyQJAHfi3E4CO9tTJ6U8WlwxEYNFL1FrqBhlmk7NYGhw6v90ucsqRUyLJI3Edtyhpb3E1YWuMBnIkrlq2ku4OVedfjQJBAPbSGyb62gwfr6ahnG7tONLwh/7V2tRxbpPph1F9j6kVcJQ3VzEFJBUhxsQbNsfdhC9Vvp3HsMcQfjkODRwF12ECQFVxD45ePn/vWrTYHyROiPTnMDBrUti9Lvf9G/mSZIL/MZIUE24hWv3KTxUd4fSP9eDf+7fVrKU95GhBVQepelQ='
        self.host = 'https://test-gateway-api.zhbtest.com'

        # 正式下單
        # self.mch_id = 'A11337'
        # self.md5_key = 'e319cb7296d04435bfd659f9c03c8cf3'
        # self.token = 'c7ac3ab1-f6ce-4a74-b49c-3b5b5552e1cd'
        # self.rsa_pub_key = 'MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCKIs9x9/Q+/KiPbM2dBZNCilOscK1s4m3HIpJSmIXgZjcf+WbqB2e3CZQbYqMZbaXubfEZpw3Lln7pq9j91mmzhxW+nALSWUxn/U9B85n9Q54/YRF6GTqCeDBgCouYYYxTi9SzAKH5myZVt7IjyhVVHE8LJMivly7Tt+uazZ6sFQIDAQAB'
        # self.rsa_pri_key = 'MIICdgIBADANBgkqhkiG9w0BAQEFAASCAmAwggJcAgEAAoGBANpGWqn/XqyUL5lbHlO20cdLAiTIEzLOnpiUlpb16p2YrH+YO4cEECqe+OLOD/1IMuE5riH5XVineu0LIFOj9+Y/I944o3OZoD7DH8AJBDMt52IztBH9U4oWV2hwaNPuyRKObCe5q4aDpejVC2OLHIfNPiteZavT037lAD6nU7lrAgMBAAECgYBXGBd5GYKHTiGoCWmScbJG2TEjyAmRDkzOCQwFdF6HP7Ikv3ORLhfdSc15gkty/un+YGuQ9tU+WKV+DCB7/0MciWmlNHFS9//sHxmaftE79BQxfcBURsFhRmZFuWLDivudGfYvgGhvUqdI33KMxi99XwYVTuecvD8+Ku+WqqswoQJBAPaFJQw/zptJqwDcN2JIBexNaAbiS2l/pU/iairbqQ4IrttDgOIWGkmiQ5R6Z/mWAvTxk5hiiRQhwfDHO5OECcMCQQDiqyZx5Ag1bP6N30WbhMyAeCX5gPOteuK4t3vHVpI4YJtAKBvXrqTC2S67Moyf6eh1qeyj6mQWIyg/QM75Zm85AkA79X5hUFOsKWrSNr2xxdrK8rjOk9PLwSQwHd28ttiTdUEyS2TZmI6kQjc1seAAMKBfezJu6eh1YRCOw6aV5pOJAkADQ9PZ8B7uJhPEl2K5SsBnWVOytFjONubtIjd2N5kDluClm+5KvQlChT5XE/NSmlvu1fPCqK2oY/lAb/6LOR6BAkEAgnw5BGA6eZQx0Iu5Sri3U6APk7oQedKhAccRq8Fc0EUMtaboS1YZpnertRPL/SrKxD5oGNBbbH4pxMZ13hlt2A=='
        # self.host = 'https://test-gateway-api.zhbtest.com'

        # RSA
        self.rsa: BaseCipher = cipher.rsa(public_key=self.rsa_pub_key, private_key=self.rsa_pri_key)

    def pre_source(self, params) -> str:
        keys = sorted([k for k in params], key=str.lower)
        source = "&".join((f"{k}={params[k]}" for k in keys if params[k] != ''))
        return source

    def sign(self, params) -> str:
        pre_source = self.pre_source(params)
        source = pre_source + f'&token={self.token}&sign={self.md5_key}'
        print('SOURCE==>', source)
        m = hashlib.md5(source.encode("utf8"))
        sign = m.hexdigest()
        print('數位簽名：', sign)
        return sign

    def rsa_sign(self, source) -> str:
        key = '-----BEGIN RSA PRIVATE KEY-----\n' + self.rsa_pri_key + '\n-----END RSA PRIVATE KEY-----'
        rsakey = RSA.importKey(key)
        cipher = Cipher_pkcs1_v1_5.new(rsakey)
        sign = base64.b64encode(cipher.encrypt(source.encode('utf8')))
        return sign.decode()

    def prepare_data(self) -> dict:
        params = {}
        params.setdefault('merchantCode', self.mch_id)  # v
        params.setdefault('merchantNo', '1234567899')  # v
        params.setdefault('userId', '0')  # v
        params.setdefault('amount', '100')  # v
        params.setdefault('coinUnit', 'CNY')  # v
        params.setdefault('callbackUrl', 'http://test.com/callback')  # v
        params.setdefault('issueBankCode', 'ICBC')  # v
        params.setdefault('name', '大老爸')  # v
        params.setdefault('bankNo', '5149588888888887')  # v
        params.setdefault('channelGroup', '0')  # v
        params.setdefault('callbackDataFormat', 'JSON')  # v
        sign = self.sign(params)
        params.setdefault('sign', sign)
        return params

    def platform_transfer(self, params=None, **kwargs):
        """代付提交接口"""
        url = self.host + '/api/rmb/issue'
        transfer_data = self.pre_source(params)
        message: Message = self.rsa.encrypt(transfer_data)
        trans_data = message.result
        print('trans_data==>', trans_data)
        result: dict = self.request(url, payload={'data': trans_data}, **kwargs)
        return result

    def set_headers(self):
        return {'token': self.token}

    def decrypt(self, data) -> dict:
        cipher_text = data.get('data')
        d: dict = php.rsa_decrypt(cipher_text=cipher_text, key=self.rsa_pub_key, key_type='public')
        return d

    def request(self, url, payload, **kws):
        headers = self.set_headers()
        resp = requests.post(url=url, json=payload, headers=headers)
        print('resp===>', resp)
        data = resp.json()
        print('data===>', data)
        return data

    def transfer(self):
        data = self.prepare_data()
        resp_data = self.platform_transfer(data)
        cred = self.decrypt(resp_data)
        print('cred===>', cred)
        return cred

    def on_notify(self):
        data = {'orderNo': '62203010434138790886230', 'data': 'Fz8gjylQY0ZXblCt2nAJfke2Qpt1xRJ06cfPpl/5JuRPmSm8H6PebMf6cNnRPx1s8q0hjwC4FJ69It3Wg1UrCXJZn1uqpOb6dYy9LsjCd5ZYyfeEOxhvY0BSAm9v7HPUkpV2zUfHhB1RhlEXuxB+UEvDycdH+3h29w4+/c/brhi3WciBbSyrdYIbGc7jQHYfnHESUMTSKdXZ9Dg5FQN74bCBHT4/l0ug9zm5fWMtSmHq0MlrO5KLtkknmfMz7ARzcIpWBt9KJMxAPdJVNTjo3ZOoz9dT84DBLOdE5zVVA4/+t/5zS1ZC9zyz77zVRNWd9kgzWw7esRWfIuDwH/0yYw==', 'merchNo': 'A16'}
        cipher_text = data.get('data')
        d: dict = php.rsa_decrypt(cipher_text=cipher_text, key=self.rsa_pri_key, key_type='private')
        print('data===>', d)

    def query(self):
        data = {'data': 'G4sALSfmxwy8AukKBiYkMuJAD+Yxn/bd9QuoP9hAaasNmFa71Nmv1hMRbGtyiSzZpGL05pfvojmvmE5udxO1hXDxybM/guRbrvn4kWCSQevpd2+SZiVFPiTakPYQsZ6ciAzEPYE/IfH40y1rZ5WYRJAf05VgXBaIZjyuzskz+VYlKIpXPfCh4vhul3fVSEokBepZTZk68WhnFsoONRuo7WDbD2owAufoPh4fyCgKMMKW9x5FefC5IpdDhNUvrAedpa7R7StZS1CAtrfyK0CNTpRq9MZdPyAvN1DR53FdCbCxXCcNIha8T8/dYNlyg2eqxNnrBD0uwDRFh+/Eu2pl6Q==', 'merchNo': 'A16', 'orderNo': '62304120541374501969283'}
        cipher_text = data.get('data')
        d: dict = php.rsa_decrypt(cipher_text=cipher_text, key=self.rsa_pub_key, key_type='public')
        print('data===>', d)


payment = Demo()


if __name__ == '__main__':
    # payment.transfer()
    # payment.on_notify()
    payment.query()

    # test_data = {"notify_key": "MIICdwIBADANBgkqhkiG9w0BAQEFAASCAmEwggJdAgEAAoGBAPb5gvFOV95Umh6+AqEwyugfJch/O/rP7FVLDDiQEA0/62KK4ej1zxBx9tKGhYE87C3ba0hAiajew5YnJN73prVv2stYqwH0GkKU6C1VZF5+VI+lfX8JcCU3SLrYtCrRQ9IIJX5K35hDZmKvriFmiaI2yrZ7ATZbv1QwmWBhB/PbAgMBAAECgYEA6plWjbs6ckHw6FTbkJwVkerMbCiYJAZP2zFfmXcXGE7oXAHK2AxutZNbvtzzgjEJtAGiZc6QNO3t4fqq5nVeT0sKoxSp530a0kicdW9rJAeWU69Pt4Pt2dpWh0TIwZM40V4Tmk2MpD746MYc0ONuDS+hvvA5MT+n0O5JuYvQkFECQQD9c3MGhz/dPe1OlW9B1B08gRyHQjWLtRrstODMrccwBtChfsgZgSpJ70IB64oi1lco7LDavsP2uyAYdvU664CDAkEA+XVjSXibChDxk1OAyKgOBhHC8lTnKyz4lUurx1vFN7/MHWdm6o5d8DMmKQjm814mjQ87H1cFymhngVXiUdgvyQJAHfi3E4CO9tTJ6U8WlwxEYNFL1FrqBhlmk7NYGhw6v90ucsqRUyLJI3Edtyhpb3E1YWuMBnIkrlq2ku4OVedfjQJBAPbSGyb62gwfr6ahnG7tONLwh/7V2tRxbpPph1F9j6kVcJQ3VzEFJBUhxsQbNsfdhC9Vvp3HsMcQfjkODRwF12ECQFVxD45ePn/vWrTYHyROiPTnMDBrUti9Lvf9G/mSZIL/MZIUE24hWv3KTxUd4fSP9eDf+7fVrKU95GhBVQepelQ=", "zf_r_pub_key": "MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCuw7gGZyNT0855KkpkVoPjtOLnPXe08pyGZVf74/hzgLWAUUcpxbK5TJLz7eTh6rKKUdpoJ/6wtPvh0khKyHDv5sXR1C2cGJk73di5+f4S9s+/i3nmNx2SU9Fm4s5IhbMwDJfWon5pnvk6uzl3GTMDqKuHXEim8e/Ar9mQ/HTugwIDAQAB", "df_r_pub_key": "MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCinWLwAHERO8tBVfTHdkZIOF7VSKQr04auwTR39MruGtqXbmvbzTd5omLm6wNbEc3X9mJ1x2ckbR/RQVp0plG6swZLFvSzo7XW6X9spAM4kC+8nj/tqF7cSET8wEwQ3gcEpC2R1vfFkM/iQtyu6CJbxccsuPGiqAKJOiYOl+qMUwIDAQAB", "token": "48692ade-e76f-4a1e-9a86-af4e7c8bd84a"}
