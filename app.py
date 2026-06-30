from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, MemberJoinedEvent
import json
import os

app = Flask(__name__)

CHANNEL_SECRET       = "4df45e7fede08b0937a9bd16f8685d89"
CHANNEL_ACCESS_TOKEN = "DMDZwNAGuXgc1Sy6RelP9f1ZsA9nFAV6p6uyF4YRw2R8Tq458nu50VEtYbAigL6Dtp+4ui91Xcdhd1iUBGbzrhYXF+y0Q1+PhjjOcL098XSSfaVnLU+0HJ0BpKJs3E8Cm8UYhc1xyeUkrFaNTlOM+QdB04t89/1O/w1cDnyilFU="
ADMIN_PASSWORD       = "你自己設一個密碼"

DATA_FILE = "members.json"

line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)
handler      = WebhookHandler(CHANNEL_SECRET)


def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []


def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


@app.route("/webhook", methods=['POST'])
def webhook():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'


@handler.add(MemberJoinedEvent)
def handle_member_joined(event):
    group_id = event.source.group_id
    data = load_data()

    for member in event.joined.members:
        user_id = member.user_id
        try:
            profile = line_bot_api.get_group_member_profile(group_id, user_id)
            display_name = profile.display_name
        except Exception:
            display_name = "(無法取得名稱)"

        order = len(data) + 1
        data.append({"order": order, "name": display_name})

    save_data(data)


@app.route("/list")
def list_members():
    password = request.args.get("pw", "")
    if password != ADMIN_PASSWORD:
        return "密碼錯誤", 403

    data = load_data()
    rows = "".join(
        f"<tr><td>{item['order']}</td><td>{item['name']}</td></tr>"
        for item in data
    )
    html = f"""
    <html><body>
    <h2>群組加入名單（共 {len(data)} 人）</h2>
    <table border="1" cellpadding="8">
    <tr><th>順序</th><th>名稱</th></tr>
    {rows}
    </table>
    </body></html>
    """
    return html


if __name__ == "__main__":
    app.run(port=5000)
