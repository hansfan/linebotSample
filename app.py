from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *


#======這裡是呼叫的檔案內容=====
from message import *
from new import *
from Function import *
#======這裡是呼叫的檔案內容=====

#======python的函數庫==========
import tempfile, os
import datetime
import time
#======python的函數庫==========
#app = Flask(__name__,template_folder='templates')
app = Flask(__name__)
static_tmp_path = os.path.join(os.path.dirname(__file__), 'static', 'tmp')
# Channel Access Token
line_bot_api = LineBotApi('wjdFptfUhAOnuKvv0OXy94a1xf6EZCZfzbkQQTU3/ylnfsIayK9GcsXE4Y1Kp+Ppx9RB9aMzxcl5+jEuSAJdjg7yEVVoPBxW7MDgv43HvKH4m3BZ7jYGTKDrdn3MZ9sLfmA+JwEz5mVHc60sR8pAhgdB04t89/1O/w1cDnyilFU=')
# Channel Secret
handler = WebhookHandler('7f17d8122a657e4f72ce0fef281d7671')

#wake up for heroku
import threading
import requests
def wake_up_heroku():
    while true :
        url = 'https://linerobotone.herokuapp.com/'+'heroku_wake_up'
        res = requests.get(url)
        if res.status_code==200:
            print('Wake up!!')
        else :
            print('Wake up - fail !!')
            time.sleep(28*60)

#threading.Thread(target=wake_up_heroku()).start()


@app.route("/heroku_wake_up")
def wake_up():
    return "wake up !!"

# 監聽所有來自 /callback 的 Post Request
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
        abort(400)
    return 'OK'


# 處理訊息
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    msg = event.message.text
    if '1' in msg:
        message = imagemap_message()
        line_bot_api.reply_message(event.reply_token, message)
    elif '2' in msg:
        message = buttons_message()
        line_bot_api.reply_message(event.reply_token, message)
    elif '3' in msg:
        message = Confirm_Template()
        line_bot_api.reply_message(event.reply_token, message)
    elif '4' in msg:
        message = Carousel_Template()
        line_bot_api.reply_message(event.reply_token, message)
    elif '5' in msg:
        message = test()
        line_bot_api.reply_message(event.reply_token, message)
    elif '6' in msg:
        message = function_list()
        line_bot_api.reply_message(event.reply_token, message)
    else:
#       do nothing 
#       message = TextSendMessage(text=msg)
#       line_bot_api.reply_message(event.reply_token, message)

@handler.add(PostbackEvent)
def handle_message(event):
    print(event.postback.data)


@handler.add(MemberJoinedEvent)
def welcome(event):
    uid = event.joined.members[0].user_id
    gid = event.source.group_id
    profile = line_bot_api.get_group_member_profile(gid, uid)
    name = profile.display_name
    message = TextSendMessage(text=f'{name}歡迎加入')
    line_bot_api.reply_message(event.reply_token, message)
        
        
import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
