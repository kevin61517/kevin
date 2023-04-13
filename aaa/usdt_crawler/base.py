import requests
import random


class Crawler:
    def __init__(self):
        self.API = 'https://www.gate.io/json_svr/query_push'

    def start(self, **kws):
        """開爬"""
        payload = self.pre_params(**kws)
        url = self._get_api()
        resp = self.request(url=url, method='POST', payload=payload)
        data = self.parse_response(resp)
        return data

    def pre_params(self, **kws):
        """前期參數準備"""
        raise NotImplementedError

    def parse_response(self, resp, **kws):
        """解析響應"""
        raise NotImplementedError

    def request(self, payload, url, method='GET', timeout=10, verify=True, **kws):
        """發送請求"""
        params = data = json = None
        if method.lower() == 'get':
            params = payload
        else:
            data = payload
        try:
            resp = self._client.request(method=method, url=url, params=params, data=data, json=json, timeout=10)
        except Exception as e:
            raise e
        try:
            resp.raise_for_status()
        except Exception as e:
            raise e
        return resp

    def _get_api(self):
        us = [20, 29]
        index = random.randint(0, 1)
        c = random.randint(10000, 900000)
        return self.API + f'/?u={us[index]}&c={c}'

    @property
    def _client(self):
        """客製化 headers 設置"""
        s = requests.Session()
        s.headers.update({'user-agent': 'DEEP_OCEAN_BOMB'})
        return s

