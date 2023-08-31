"""
============================
# @Time    : 2023/8/30 16:45
# @Author  : Elaikona
# @FileName: chat_center.py
===========================
"""
from message.models import Room, UserRoomShip


def create_room(user_id, name, room_type, team):
    room = Room.objects.create(roomName=name, type=room_type, team=team)
    UserRoomShip.objects.create(user_id=user_id, room=room, identify=UserRoomShip.Identify.CREATOR)
    return room


def join_room(user_id, room):
    UserRoomShip.objects.create(user_id=user_id, room=room, identify=UserRoomShip.Identify.NORMAL)
