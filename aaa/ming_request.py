"""
http = Hyper Text Transport Protocol 超文本傳輸協議
ngrok說明：
簡介:
 - 一個可以暫時讓自己本地連限制網際網路的方法：ngrok(需要安裝 brew install ngrok)

如何使用: [我是參數] 表示傳遞參數。
 - ngrok http [port] -> Example ngrok http 6666: 當本地服務器啟用時HOST=0.0.0.0 然後 port=6666。
 - 啟用成功時會出現 http://6cf9-118-167-143-56.ngrok.io -> http://localhost:6666  (Forwarding)
 表示 「->」 左方的 [HOST] 暫時會指向到 http://localhost:6666 port下，就可以讓外部的請求測試。
"""
import requests
import uuid
import hashlib
import time
import json

if __name__ == '__main__':
    url = 'https://q3.bj-huishou.com/games.json'
    resp = requests.get(url)
    data = resp.json()
    games = data
    n = 0
    for game in games:
        platform = game.get('platform')
        code = game.get('code')
        name = game.get('name')
        if 'PT' in platform or 'GMMG' in platform:
            print('遊戲廳：', platform, '|', '遊戲碼：', code, '|', '遊戲名：', name)
