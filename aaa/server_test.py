from flask import Flask, jsonify, request, Request, Response
import time
from payment_test import Payment

app = Flask(__name__)

config = {
    'mch_id': 'A230425203209361',
    'key': '7fdb56f490644a9f8511f8a2c6198ebc',
    'aes_key': '57xuEaVXYf6Lq7AL',
    'url': 'https://api.doudoupays.com/gateway/pay/deposit',
}


@app.route("/test_get")
def test_get():
    print('== SERVER 被請求 ==')
    results = []
    for num in range(3):
        data = {
            'date': '2022-06-19',
            'production': 'TXF',
            'type': 100 + num,
            'time': int(time.time())
        }
        results.append(data)
    return jsonify(code=200, data=results)


@app.route("/test_post", methods=["POST"])
def test_post():
    data = request.form
    r: Request = request
    print(request)
    print('data===>', data)
    return jsonify(code=200, data='SUCCESS')


@app.route("/test/pay")
def test_pay():
    """測試下單"""
    payment = Payment(**config)
    pay_data = request.json
    result = payment.pay(pay_data)
    return jsonify(code=200, data=result)


@app.route("/test/notify", methods=["POST"])
def test_notify():
    """測試回調"""
    try:
        data = request.form.to_dict()
    except Exception as e:
        data = {}
    print('11111')
    payment = Payment(**config)
    result = payment.notify(data)
    return jsonify(code=200, data=result)


@app.route("/test/notify/ping", methods=["POST"])
def test_notify_ping():
    """測試測試回調"""
    return jsonify(code=200, data='pong')


@app.route("/test/k", methods=["POST"])
def kkk():
    """測試測試回調"""
    try:
        data = request.json
    except:
        data = request.args.to_dict() or request.form.to_dict()
    print('data==>', data)
    return jsonify(code=200, data='pong')

# """
# DOMAIN(HOST) + API:
# http://taiwan/taipei/zseastroad_1/14/1f
# """
# """中華民國台北市忠孝東路一段14號1樓"""
# """中華民國台北市忠孝東路一段14號2樓"""
if __name__ == '__main__':
    app.run(host='0.0.0.0', port='6666', debug=True)
