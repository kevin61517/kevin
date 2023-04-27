from ciphers import cipher, AES
import requests

aes_key = ''
aes = cipher.aes(key='57xuEaVXYf6Lq7AL', mode=AES.MODE_ECB)


data = {'content': 'lks4eIlgoyHxpKMEhJqNQ7XuGWCsThARkAbdTr2qXyDjtPLSGWgd4ocuMmJTJ9mvuFUtnsqMaa27dubDCkjT5GbishGEWsTO4L1+gYEDVYvHa6H8xd6ZJLABEbihlxzouxYf6vqUJYMzTz+NBHlNhneZmFyJrvc1Arh+qM2C2MeT9kkBCBy581uzSJZBF5FPIP74hvpBZ0S+Qc42W3KIkZ65R8M1AVGjHWpI549sE7aRWrotLznlt+J37cxO5r/6eC9Q69SXqMutjMjziPGa/R0938Dm8l0gvI5kn98LAe8='}
data['mno'] = 'A230425203209361'

if __name__ == '__main__':
    resp = requests.post(url='http://lc.api-go-pay.com', data=data)
    print('resp==>', resp)
    print('返回資料：', resp.json())
    message = aes.decrypt(data['content'])
    print(message.result)
