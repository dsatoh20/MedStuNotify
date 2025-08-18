from users.bot_base import LineBotMSG
from users.models import User
from .models import Lecture
from rest_framework import permissions, viewsets
from rest_framework.response import Response
from .serializers import LectureSerializer
from rest_framework.decorators import api_view


class LectureViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Lecture.objects.all().order_by('-created_at')
    serializer_class = LectureSerializer
    permission_classes = [permissions.AllowAny]

@api_view(['POST'])
def NotifyView(request):
    """
    Lecturesに新規登録があった場合、LINEに通知する。
    """
    incoming_lectures = request.data
    if not incoming_lectures:
        return Response("No data provided.", status=400)

    # 既存の講義を一度にすべて取得（タプルのセットにして高速検索）
    existing_lectures = set(Lecture.objects.values_list('grade', 'subject', 'content'))

    new_lectures_to_create = []
    for lecture_data in incoming_lectures:
        # 比較用のタプルを作成
        lecture_tuple = (
            lecture_data['grade'],
            lecture_data['subject'],
            lecture_data['content']
        )
        
        # 既存のセットになければ、新規講義と判断
        if lecture_tuple not in existing_lectures:
            new_lectures_to_create.append(
                Lecture(
                    grade=lecture_data['grade'],
                    subject=lecture_data['subject'],
                    content=lecture_data['content']
                )
            )

    # 新規講義がなければ、ここで処理を終了
    if len(new_lectures_to_create) == 0:
        print('No new lectures found.')
        return Response("No new lectures to process.", status=200)

    # 3. パフォーマンス改善：bulk_createで新規講義を一括登録
    Lecture.objects.bulk_create(new_lectures_to_create)
    print(f"{len(new_lectures_to_create)} new lectures created.")

    # 新規登録されたものだけを対象に通知処理
    for new_lecture in new_lectures_to_create:
        targeted_users = User.objects.filter(grade=new_lecture.grade)
        if targeted_users.exists():
            userid_list = [user.userId for user in targeted_users]
            msg = f"【講義変更】\n学年: {new_lecture.grade}\n科目: {new_lecture.subject}\n内容: {new_lecture.content}"
            
            linebot = LineBotMSG(msg)
            linebot.multicast(userid_list)
            
            print(f"Notification for '{new_lecture.subject}' sent to {len(userid_list)} users.")
        else:
            print(f"No users found for grade {new_lecture.grade}.")
            
    return Response("Completed notification process.", status=200)