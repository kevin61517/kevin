from base import Crawler


class USDT(Crawler):

    def pre_params(self, **kws):
        """前期參數準備"""
        return {'type': 'push_main_rates', 'symbol': 'USDT_CNY'}

    def parse_response(self, resp, **kws):
        """解析響應"""
        data = resp.json()
        if not data.get('result'):
            raise ValueError('Request false.')
        return data.get('appraised_rates')
