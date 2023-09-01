"""
============================
# @Time    : 2023/8/26 14:40
# @Author  : Elaikona
# @FileName: chat.py
===========================
"""
import logging
import os

from django.db.models import Q
from rest_framework.decorators import api_view

from MewTeam import settings
from message.models import Room, UserRoomShip, Message, MessageFile
from message.serializers import RoomSerializer, MessageSerializer, MessageFileSerializer
from shared.chat_center import create_room
from shared.error import Error
from shared.random import generate_session_id
from shared.res_temp import ResponseTemplate
from shared.token import check_token
from team.models import Team
from user.models import User
from user.serializers import UserSerializer

logger = logging.getLogger('__name__')


@api_view(['POST'])
def upload_message_file(request):
    try:
        response, user_id = check_token(request)
        if user_id == -1:
            return response
        mid = request.POST.get("mid", None)
        file = request.FILES.get('file', None)
        print(file)
        if file is None:
            return ResponseTemplate(Error.FILE_MISSING, 'Missing file')
        if file.size > settings.MAX_MESSAGE_FILE_SIZE:
            return ResponseTemplate(Error.FILE_SIZE_ILLEGAL, 'Size of file is too large. It should be less than 64mb.')
        filepath = f"{settings.MESSAGE_ROOT}{mid}/{file.name}"
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, "wb+") as f:
            for chunk in file.chunks():
                f.write(chunk)
        return ResponseTemplate(Error.SUCCESS, 'upload file successfully')
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


@api_view(['POST'])
def create_private_room(request, team_id):
    try:
        response, current_user_id = check_token(request)
        if current_user_id == -1:
            return response
        user_id = request.data['user_id']
        user1 = User.objects.get(id=current_user_id)
        user2 = User.objects.get(id=user_id)
        room = Room.objects.create(roomName=f"{user1.name}和{user2.name}的会话", type=Room.RoomType.PRIVATE,
                                   team_id=team_id)
        UserRoomShip.objects.create(room=room, user=user1, identify=UserRoomShip.Identify.NORMAL)
        UserRoomShip.objects.create(room=room, user=user2, identify=UserRoomShip.Identify.NORMAL)
        return ResponseTemplate(Error.SUCCESS, 'success create private room')
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


@api_view(['GET'])
def search_history_message(request, room_id):
    try:
        response, user_id = check_token(request)
        if user_id == -1:
            return response
        keyword = request.query_params.get('keyword', None)
        if keyword and keyword != "":
            query = Q(content__icontains=keyword)
        else:
            query = Q()  # 空查询，返回所有消息
        messages = Message.objects.filter(room_id=room_id).filter(query).all()
        return ResponseTemplate(Error.SUCCESS, 'search history success',
                                data=MessageSerializer(messages, many=True).data)
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


@api_view(['GET'])
def get_create_private_group_user_list(request, team_id):
    try:
        response, current_user_id = check_token(request)
        if current_user_id == -1:
            return response
        team = Team.objects.filter(id=team_id).first()
        ships = team.userteamship_set.all()

        current_user_private_ships = UserRoomShip.objects.filter(user_id=current_user_id,
                                                                 room__type=Room.RoomType.PRIVATE,
                                                                 room__team_id=team_id).all()
        exist_private_user_id_list = []
        for ship in current_user_private_ships:
            for room_ship in ship.room.userroomship_set.all():
                if room_ship.user_id != current_user_id:
                    exist_private_user_id_list.append(room_ship.user_id)

        users_info = []
        for ship in ships:
            if ship.user.id != current_user_id and ship.user.id not in exist_private_user_id_list:
                users_info.append(UserSerializer(ship.user).data)
        return ResponseTemplate(Error.SUCCESS, 'success', data=users_info)
    except Exception as e:
        return ResponseTemplate(Error.FAILED, str(e))
