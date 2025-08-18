from .bot_base import LineBotMSG
from .models import User
from rest_framework import permissions, viewsets
from rest_framework.views import APIView
from rest_framework.response import Response

from .serializers import UserSerializer

from pathlib import Path
import environ
import os

BASE_DIR = Path(__file__).resolve().parent.parent
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))
env = environ.Env()


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-created_at')
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]


msg_to_activate = env('MSG_TO_ACTIVATE')


class LINEAPIView(APIView):
    def post(self, request, *args, **kwargs):
        res = request.data
        if len(res['events']) == 0: # イベントがない場合
            return Response("No events found", status=200)
        data = res['events'][0] #リストの中に辞書がひとつ
        reply_token = data['replyToken'] # for reply
        if data['type'] != 'message': # messageでない場合
            return Response("No message event", status=200)
        
        print("Message recieved.")
        print(data)
        text = data['message'].get('text')
        userid = data['source']['groupId'] or data['source']['roomId'] or data['source']['userId']

        # msg_to_activateがメッセージの先頭にあるか確認
        if not text.startswith(msg_to_activate):
            print(f"Message does not start with {msg_to_activate}.")
            return Response("No message for this bot", status=200)
        # 学年を設定する
        try:
            # メッセージをスペースで分割し、最後の要素を学年とする
            grade_str = text.strip().split()[-1]
            grade = int(grade_str)
        except (ValueError, IndexError):
            print("Invalid grade input.")
            msg = f"`{msg_to_activate}`に続いて、学年を半角数字で入力してください：\n 例：`{msg_to_activate} 3`."
            linebot = LineBotMSG(msg)
            linebot.reply(reply_token)
            return Response("Invalid grade format", status=400)

        _, created = User.objects.update_or_create(
            userId=userid,
            defaults={'grade': grade}
        )
        if created: # 新規ユーザーを登録
            print(f"New user created: {userid}")
            msg = f"学年を{grade}に設定しました。"
            linebot = LineBotMSG(msg)
            linebot.reply(reply_token)
        else: # 既存ユーザーは学年を更新
            print(f"User updated: {userid}")
            msg = f"学年を{grade}に更新しました。"
            linebot = LineBotMSG(msg)
            linebot.reply(reply_token)
        return Response("OK", status=200) # 登録/更新が成功したらOKを返す