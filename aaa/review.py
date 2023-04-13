from __future__ import unicode_literals
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import configparser
import random
from pprint import pprint

app = Flask(__name__)

# LINE 聊天機器人的基本資料
config = configparser.ConfigParser()
config.read('config.ini')

line_bot_api = LineBotApi(config.get('line-bot', 'channel_access_token'))
handler = WebhookHandler(config.get('line-bot', 'channel_secret'))

# ========================ORI CODE =======================================


# 接收 LINE 的資訊
@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']

    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    try:
        print(body, signature)
        handler.handle(body, signature)

    except InvalidSignatureError:
        abort(400)

    return 'OK'


# 學你說話
@handler.add(MessageEvent, message=TextMessage)
def pretty_echo(event):
    if event.source.user_id != "Udeadbeefdeadbeefdeadbeefdeadbeef":

        # Phoebe 愛唱歌
        pretty_note = '♫♪♬'
        pretty_text = ''

        if event.message.text == '我':
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text="yu chen is gay")
            )

        for i in event.message.text:
            pretty_text += i
            pretty_text += random.choice(pretty_note)

        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=pretty_text)
        )
        print('here', event.message.text)

# ========================ORI CODE =======================================




# ========================== class mode =======================================

# class FlaskMain:
#
#     app = Flask(__name__)
#     config = configparser.ConfigParser()
#     config.read('config.ini')
#     line_bot_api = LineBotApi(config.get('line-bot', 'channel_access_token'))
#     handler = WebhookHandler(config.get('line-bot', 'channel_secret'))
#
#     @staticmethod
#     @app.route("/callback", methods=['POST'])
#     def callback():
#         signature = request.headers['X-Line-Signature']
#         body = request.get_data(as_text=True)
#         FlaskMain.app.logger.info("Request body: " + body)
#         try:
#             print(body, signature)
#             FlaskMain.handler.handle(body, signature)
#
#         except InvalidSignatureError:
#             abort(400)
#
#         return 'OK'
#
#     @handler.add(MessageEvent, message=TextMessage)
#     def echo(self, event):
#
#         if event.source.userid != "Udeadbeefdeadbeefdeadbeefdeadbeef":
#
#             # Phoebe 愛唱歌
#             pretty_note = '♫♪♬'
#             pretty_text = ''
#
#             if event.message.text == '我':
#                 FlaskMain.line_bot_api.reply_message(
#                     event.reply_token,
#                     TextSendMessage(text="yu chen is gay")
#                 )
#             else:
#
#                 for i in event.message.text:
#                     pretty_text += i
#                     pretty_text += random.choice(pretty_note)
#
#                 FlaskMain.line_bot_api.reply_message(
#                     event.reply_token,
#                     TextSendMessage(text=pretty_text)
#                 )
#                 print('here', event.message.text)
#
#
# if __name__ == "__main__":
#
#     app = FlaskMain()
#     app.app.run(host='0.0.0.0', port=5001, debug=True)

# ========================== class mode =======================================