"""
============================
# @Time    : 2023/8/26 14:40
# @Author  : Elaikona
# @FileName: chat.py
===========================
"""
import os

from rest_framework.decorators import api_view

from MewTeam import settings
from message.models import MessageFile, Session
from message.serializers import SessionSerializer, MessageSerializer
from shared.error import Error
from shared.random import generate_session_id
from shared.res_temp import ResponseTemplate
from shared.token import check_token
from user.models import User


@api_view(['POST'])
def upload_message_file(request):
    try:
        response, user_id = check_token(request)
        if user_id == -1:
            return response
        mid = request.POST.get("mid")
        file = request.FILES.get('file')
        if file is None:
            return ResponseTemplate(Error.FILE_MISSING, 'Missing file')
        if file.size > settings.MAX_MESSAGE_FILE_SIZE:
            return ResponseTemplate(Error.FILE_SIZE_ILLEGAL, 'Size of file is too large. It should be less than 64mb.')
        filepath = f"{settings.MESSAGE_ROOT}/{mid}/{file.name}"
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, "wb+") as f:
            for chunk in file.chunks():
                f.write(chunk)
        return ResponseTemplate(Error.SUCCESS, 'upload file successfully')
    except Exception as e:
        return ResponseTemplate(Error.FAILED, str(e))


@api_view(['POST'])
def get_session_id(request):
    try:
        response, user_id = check_token(request)
        if user_id == -1:
            return response
        target_user_id = request.data['target_user_id']
        user1 = User.objects.get(id=user_id)
        user2 = User.objects.get(id=target_user_id)
        session = Session.objects.filter(users=user1).filter(users=user2).first()
        if session is None:
            session = Session.objects.create(session_id=generate_session_id())
            session.users.add(user1, user2)
        return ResponseTemplate(Error.SUCCESS, 'get session info successfully', data=SessionSerializer(session).data)
    except Exception as e:
        return ResponseTemplate(Error.FAILED, str(e))


@api_view(['GET'])
def get_private_chat_sessions(request):
    try:
        response, user_id = check_token(request)
        if user_id == -1:
            return response
        user = User.objects.get(id=user_id)
        sessions = Session.objects.filter(users=user).all()
        return ResponseTemplate(Error.SUCCESS, 'get session list successfully',
                                data=SessionSerializer(sessions, many=True).data)
    except Exception as e:
        return ResponseTemplate(Error.FAILED, str(e))


@api_view(['GET'])
def get_private_chat_history(request, session_id):
    try:
        response, user_id = check_token(request)
        if user_id == -1:
            return response
        session = Session.objects.get(session_id=session_id)
        messages = session.message_set.order_by('-timestamp')[:100]
        return ResponseTemplate(Error.SUCCESS, 'get private chat history messages successfully',
                                data=MessageSerializer(messages, many=True).data)
    except Exception as e:
        return ResponseTemplate(Error.FAILED, str(e))
