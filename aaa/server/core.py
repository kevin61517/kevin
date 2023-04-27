data = {
        "merchno": "0e4b9f5cfb",
        "orderId": "123456787",
        "requestCurrency": "1",
        "asyncUrl": "http://82c4-18-163-217-66.ngrok.io/api/payment/callback/Cuicanxing",
        "syncUrl": "http://82c4-18-163-217-66.ngrok.io/api/payment/callback/Cuicanxing",
        "amount": "200.00",
        "requestTime": "20230421121157",
        "apiVersion": "2",
        "payType": "0",
        "attach": "",
        "post_url": "https://api.cuicanxing888.com/api/order/placeOrder",
        "sign": "5238320b15793d82be8c8fb63feac938"
    }
s = '&'.join((f'{k}={v}' for k, v in data.items()))

r = {'amount': ['1000.00'], 'apiVersion': ['2'], 'attach': ['大老爸'], 'merchno': ['0e4b9f5cfb'], 'orderId': ['123456789'], 'payType': ['3'], 'requestCurrency': ['1'], 'sign': ['adbc263a49c4cd18ba99a89192c79fa7'], 'status': ['2']}


if __name__ == '__main__':
    print('http://0.0.0.0:5000/payment/redirect?'+s)
    # print({k: v[0] for k, v in r.items()})
