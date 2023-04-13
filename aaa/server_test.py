from flask import Flask, jsonify, request, Request, Response
import time

app = Flask(__name__)


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


# """
# DOMAIN(HOST) + API:
# http://taiwan/taipei/zseastroad_1/14/1f
# """
# """中華民國台北市忠孝東路一段14號1樓"""
# """中華民國台北市忠孝東路一段14號2樓"""
if __name__ == '__main__':
    app.run(host='0.0.0.0', port='6666', debug=True)
