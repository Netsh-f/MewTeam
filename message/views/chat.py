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
from message.models import Room, UserRoomShip, Message
from message.serializers import RoomSerializer, MessageSerializer, MessageFileSerializer
from shared.chat_center import create_room
from shared.error import Error
from shared.random import generate_session_id
from shared.res_temp import ResponseTemplate
from shared.token import check_token
from team.models import Team
from user.models import User
from user.serializers import UserSerializer
from datetime import datetime, timedelta


@api_view(['POST'])
def upload_message_file(request):
    try:
        response, user_id = check_token(request)
        if user_id == -1:
            return response
        mid = request.POST.get("mid")
        file = request.FILES.get('file')
        print(file)
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
        session = Room.objects.filter(users=user1).filter(users=user2).first()
        if session is None:
            session = Room.objects.create(session_id=generate_session_id())
            session.users.add(user1, user2)
        return ResponseTemplate(Error.SUCCESS, 'get session info successfully', data=RoomSerializer(session).data)
    except Exception as e:
        return ResponseTemplate(Error.FAILED, str(e))


@api_view(['GET'])
def get_private_chat_sessions(request):
    try:
        response, user_id = check_token(request)
        if user_id == -1:
            return response
        user = User.objects.get(id=user_id)
        sessions = Room.objects.filter(users=user).all()
        return ResponseTemplate(Error.SUCCESS, 'get session list successfully',
                                data=RoomSerializer(sessions, many=True).data)
    except Exception as e:
        return ResponseTemplate(Error.FAILED, str(e))


@api_view(['GET'])
def get_private_chat_history(request, session_id):
    try:
        response, user_id = check_token(request)
        if user_id == -1:
            return response
        session = Room.objects.get(session_id=session_id)
        messages = session.message_set.order_by('-timestamp')[:100]
        return ResponseTemplate(Error.SUCCESS, 'get private chat history messages successfully',
                                data=MessageSerializer(messages, many=True).data)
    except Exception as e:
        return ResponseTemplate(Error.FAILED, str(e))


@api_view(['POST'])
def create_group(request, team_id):
    try:
        response, current_user_id = check_token(request)
        if current_user_id == -1:
            return response
        name = request.data['name']
        users_info = request.data['users']
        team = Team.objects.get(id=team_id)
        room = create_room(user_id=current_user_id, name=name, room_type=Room.RoomType.GROUP, team=team)
        for user_info in users_info:
            user_id = user_info['id']
            UserRoomShip.objects.create(user_id=user_id, room=room, identify=UserRoomShip.Identify.NORMAL)
        return ResponseTemplate(Error.SUCCESS, 'create room successfully')
    except Exception as e:
        return ResponseTemplate(Error.FAILED, str(e))


@api_view(['GET'])
def get_room_list(request, team_id):
    try:
        response, user_id = check_token(request)
        if user_id == -1:
            return response
        ships = UserRoomShip.objects.filter(user_id=user_id, room__team_id=team_id).all()
        rooms = []
        for ship in ships:
            room_info = RoomSerializer(ship.room).data
            users_info = []
            for room_ship in ship.room.userroomship_set.all():
                users_info.append(UserSerializer(room_ship.user).data)
            room_info['users'] = users_info
            room_info['current_user_identify'] = ship.identify
            rooms.append(room_info)
        return ResponseTemplate(Error.SUCCESS, 'get room list', data=rooms)
    except Exception as e:
        return ResponseTemplate(Error.FAILED, str(e))


@api_view(['GET'])
def get_chat_history(request, room_id):
    try:
        response, user_id = check_token(request)
        if user_id == -1:
            return response
        earliest_message_id = request.query_params.get('earliest_message_id', None)
        if earliest_message_id:
            messages = Message.objects.filter(room_id=room_id, id__lt=earliest_message_id).order_by('-timestamp')[:50][
                       ::-1]
        else:
            messages = Message.objects.filter(room_id=room_id).order_by('-timestamp')[:50][::-1]
        messages_info = []
        for message in messages:
            message_info = MessageSerializer(message).data
            message_info['files'] = MessageFileSerializer(message.messagefile_set.all(), many=True).data
            messages_info.append(message_info)
        return ResponseTemplate(Error.SUCCESS, 'success', data=messages_info)
    except Exception as e:
        return ResponseTemplate(Error.FAILED, str(e))


@api_view(['POST'])
def exit_room(request, room_id):
    try:
        response, user_id = check_token(request)
        if user_id == -1:
            return response
        ship = UserRoomShip.objects.filter(user_id=user_id, room_id=room_id).first()
        ship.delete()
        return ResponseTemplate(Error.SUCCESS, 'exit chat room successfully')
    except Exception as e:
        return ResponseTemplate(Error.FAILED, str(e))


@api_view(['POST'])
def dissolve_room(request, room_id):
    try:
        response, user_id = check_token(request)
        if user_id == -1:
            return response
        ship = UserRoomShip.objects.filter(user_id=user_id, room_id=room_id).first()
        if ship.identify != UserRoomShip.Identify.CREATOR:
            return ResponseTemplate(Error.PERMISSION_DENIED, 'you are not the creator of this team')
        room = ship.room
        room.delete()
        return ResponseTemplate(Error.SUCCESS, 'dissolve chat room successfully')
    except Exception as e:
        return ResponseTemplate(Error.FAILED, str(e))


@api_view(['GET'])
def get_create_group_user_list(request, team_id):
    try:
        response, user_id = check_token(request)
        if user_id == -1:
            return response
        team = Team.objects.filter(id=team_id).first()
        ships = team.userteamship_set.all()
        users_info = []
        for ship in ships:
            if ship.user.id != user_id:
                users_info.append(UserSerializer(ship.user).data)
        return ResponseTemplate(Error.SUCCESS, 'success', data=users_info)
    except Exception as e:
        return ResponseTemplate(Error.FAILED, str(e))
