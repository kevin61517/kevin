"""for 佳宜
1.讀取
2.行情判斷
3.進場
4.出場

裝飾器: 如何運作。

檔案傳達的想法：
1.封裝自己的功能
2.定義有效的流程
3.針對不同的市場時左不同的功能
4.用一個管理器來管理各個不同市場分析物件
5.統一一個程式入口

物件觀念：
封裝: 把一套流程封裝成一個方法，並且取一個可讀性高的名稱。
繼承: 子類別擴充於父類別。
多型: 不同子類別物件的 analysis() 方法具有不同的行為。

設計模式：
工廠模式 Factory Pattern: 定義一個物件的行為以及流程且子類別必須實作流程。
享元模式 Flyweight Pattern: 管理物件們，確保被管理的子類別不會被亂七八糟的實例(降低電腦記憶體使用量)。
"""
import sys


class BaseMarketAnalysis:
    """流程定義(基類)"""
    NAME = None

    def __init__(self):
        if self.NAME is None:
            raise TypeError('NAME argument must define.')

    def _read(self):
        """讀取資料"""
        raise NotImplementedError

    def _analysis(self):
        """分析資料"""
        raise NotImplementedError

    def _in(self):
        """進場"""
        raise NotImplementedError

    def _out(self):
        """出場"""
        raise NotImplementedError

    def analysis(self):
        """入口"""
        self._read()
        self._analysis()
        self._in()
        self._out()
        return 'success'


class AmericaMarket(BaseMarketAnalysis):
    NAME = 'america'

    def _read(self):
        print('美國市場讀取')

    def _analysis(self):
        print('美國市場分析')

    def _in(self):
        print('美國市場進場')

    def _out(self):
        print('美國市場出場')


class TaiwanMarket(BaseMarketAnalysis):
    NAME = 'taiwan'

    def _read(self):
        print('台灣市場讀取')

    def _analysis(self):
        print('台灣市場分析')

    def _in(self):
        print('台灣市場進場')

    def _out(self):
        print('台灣市場出場')


class MarketManager:
    """市場管理者"""
    def __init__(self):
        self._implemented_markets = {}  # 已經實作的市場分析
        for class_ in BaseMarketAnalysis.__subclasses__():  # BaseMarketAnalysis的子類別們(es)
            self._implemented_markets[class_.NAME.lower()] = class_()

    @property
    def markets(self):
        """檢視已經被實例的市場分析物件"""
        return [mkt for mkt in self._implemented_markets.keys()]

    def get_market(self, market_name):
        """取得市場"""
        try:
            return self._implemented_markets[market_name]
        except Exception as e:
            raise KeyError(f'Market {market_name} not implemented.')


market_manager = MarketManager()


if __name__ == '__main__':
    name = sys.argv[1]  # python3 ming.py [argv]
    market = market_manager.get_market(name)
    market.analysis()
    print(market_manager.markets)
