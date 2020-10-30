from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

app = Flask(__name__)

line_bot_api = LineBotApi('bEWUw5lOjbkRozIP5ZC+XQtj7XG9wGGbicxTOy/sEPX8NOZCi7KCjHRkwuN1Gdr+/VoqvxcnV1bCEihUKQLtmmTBMmBkOxVM/Jy61DmyA+XT2AyNjiYai+eKFzqyRxzN5vmmJfD3xx61wQ1WWJnJdAdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('3ad9d6c13d7124bc47852f00f81ee584')


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    msg = event.message.text
    r = '不好意思，我無法理解你說的內容，請你再說一次'
    if msg in [hi, Hi, 你好, ]:
        r = '你好，請問有需要幫忙嗎?'
    elif msg == '吃過飯了嗎':
        r = '還沒'
    elif msg in ['你是', '你是誰']:
        r = '我是聊天機器人'
    elif '訂位' in msg:
        r = '你想訂位，是嗎?'            
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=r))


if __name__ == "__main__":
    app.run()