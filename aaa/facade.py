"""
面板模式
"""


class TransactionServer:
    """交易服務器"""
    def __init__(self):
        self._order = Order()
        self._transfer = Transfer()

    def sell(self, amount):
        min_ = 100
        if amount < min_:
            return f'{self._order.sell_order()}失敗，金額須超過{min_}(當前掛單金額為{amount})'
        return f'{self._order.sell_order()}成功'

    def buy(self):
        return self._order.buy_order()

    def currency_transfer(self, amount):
        return self._transfer.currency(amount)

    def digital_transfer(self, amount):
        return self._transfer.digital_currency(amount)


class Order:
    """掛單、拉單"""
    def sell_order(self):
        """掛單"""
        return '掛單'

    def buy_order(self):
        """拉單"""
        return '拉單'


class Transfer:
    def currency(self, amount):
        """貨幣支付"""
        return f'支付貨幣金額{amount}'

    def digital_currency(self, amount):
        """虛擬貨幣支付"""
        return f'支付虛擬貨幣金額{amount}'


if __name__ == '__main__':
    server = TransactionServer()
    print(server.sell(20))
