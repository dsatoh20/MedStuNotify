import urllib.request
import json
from pathlib import Path
import environ
import os

from .bot_messages import create_message

BASE_DIR = Path(__file__).resolve().parent.parent
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))
env = environ.Env()

LINE_ACCESS_TOKEN = env("LINE_ACCESS_TOKEN")



REPLY_ENDPOINT_URL = "https://api.line.me/v2/bot/message/reply"
PUSH_ENDPOINT_URL = "https://api.line.me/v2/bot/message/push"
MULTICAST_ENDPOINT_URL = "https://api.line.me/v2/bot/message/multicast"

HEADER = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer ' + LINE_ACCESS_TOKEN
}

class LineBotMSG():
    def __init__(self, messages):
        self.messages = messages

    def reply(self, reply_token):
        body = {
            'replyToken': reply_token,
            'messages': create_message(self.messages)
        }
        
        req = urllib.request.Request(REPLY_ENDPOINT_URL, json.dumps(body).encode(), HEADER)
        
        try:
            with urllib.request.urlopen(req) as res:
                body = res.read()
        except urllib.error.HTTPError as err:
            print(err)
        except urllib.error.URLError as err:
            print(err.reason)
    def push(self, userid):
        body = {
            'to': userid,
            'messages': create_message(self.messages)
        }
        req = urllib.request.Request(PUSH_ENDPOINT_URL, json.dumps(body).encode(), HEADER)
        try:
            with urllib.request.urlopen(req) as res:
                body = res.read()
        except urllib.error.HTTPError as err:
            print(err)
        except urllib.error.URLError as err:
            print(err.reason)
    def multicast(self, user_list):
        body = {
            'to': user_list,
            'messages': create_message(self.messages)
        }
        req = urllib.request.Request(MULTICAST_ENDPOINT_URL, json.dumps(body).encode(), HEADER)
        try:
            with urllib.request.urlopen(req) as res:
                body = res.read()
        except urllib.error.HTTPError as err:
            print(err)
        except urllib.error.URLError as err:
            print(err.reason)