from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

app = Flask(__name__)

CHANNEL_SECRET       = "4df45e7fede08b0937a9bd16f8685d89"
CHANNEL_ACCESS_TOKEN = "DMDZwNAGuXgc1Sy6RelP9f1ZsA9nFAV6p6uyF4YRw2R8Tq458nu50VEtYbAigL6Dtp+4ui91Xcdhd1iUBGbzrhYXF+y0Q1+PhjjOcL098XSSfaVnLU+0HJ0BpKJs3E8Cm8UYhc1xyeUkrFaNTlOM+QdB04t89/1O/w1cDnyilFU="
GROUP_LINK           = "https://line.me/ti/g/CRnDKT_5RW"

line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)
handler      = WebhookHandler(CHANNEL_SECRET)

@app.route("/webhook", methods=['POST'])
def webhook():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    if "加群" in event.message.text:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=f"歡迎加入！點此連結：{GROUP_LINK}")
        )

if __name__ == "__main__":
    app.run(port=5000)