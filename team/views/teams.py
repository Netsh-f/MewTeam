import os

from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from rest_framework.decorators import api_view

from MewTeam import settings
from message.models import Room
from shared.chat_center import create_room
from shared.error import Error
from shared.res_temp import ResponseTemplate
from shared.token import check_token
from shared.validator import validate_image_name
from team.models import UserTeamShip, Team
from shared.permission import is_creator
from team.serializers import TeamSerializer


@api_view(['POST'])
def create_team(request):
    try:
        response, user_id = check_token(request)
        if user_id == -1:
            return response
        data = request.data
        name = data['name']
        with transaction.atomic():
            new_team = Team.objects.create(name=name)
            UserTeamShip.objects.create(user_id=user_id, team=new_team, identify=UserTeamShip.Identify.CREATOR)

            room = create_room(user_id=user_id, name=name, room_type=Room.RoomType.TEAM, team=new_team)
            room.avatar = new_team.avatar
            room.save()

            return ResponseTemplate(Error.SUCCESS, 'Team created successfully!', data={'team_id': new_team.id})
    except Exception as e:
        return ResponseTemplate(Error.DATABASE_INTERNAL_ERROR, str(e) + "user_id=" + str(user_id))


@api_view(['GET'])
def get_team_list(request):
    try:
        response, current_user_id = check_token(request)
        if current_user_id == -1:
            return response
        ships = UserTeamShip.objects.filter(user_id=current_user_id)
        team_list = []
        for ship in ships:
            team_list.append({
                'team': TeamSerializer(ship.team).data,
                'identity': ship.identify,
            })
        return ResponseTemplate(Error.SUCCESS, 'get current user team list successfully', data=team_list)
    except ObjectDoesNotExist as e:
        return ResponseTemplate(Error.DATABASE_INTERNAL_ERROR, str(e))
    except Exception as e:
        return ResponseTemplate(Error.FAILED, str(e))


@api_view(['DELETE'])
def disband_team(request, team_id):
    try:
        response, current_user_id = check_token(request)
        if current_user_id == -1:
            return response
        team = Team.objects.get(id=team_id)
        if not is_creator(current_user_id, team_id):
            return ResponseTemplate(Error.PERMISSION_DENIED, 'you are not the creator of the team')
        team.delete()
        return ResponseTemplate(Error.SUCCESS, 'Team disbanded successfully')
    except Exception as e:
        return ResponseTemplate(Error.FAILED, str(e))


@api_view(['POST'])
def update_team_avatar(request, team_id):
    try:
        response, current_user_id = check_token(request)
        if current_user_id == -1:
            return response
        file = request.FILES.get('file')
        if file is None:
            return ResponseTemplate(Error.FILE_MISSING, 'Missing image file')
        if not validate_image_name(file.name):
            return ResponseTemplate(Error.FILE_TYPE_INVALID, 'Invalid image file type')
        if file.size > settings.MAX_AVATAR_FILE_SIZE:
            return ResponseTemplate(Error.FILE_SIZE_ILLEGAL, 'Size of file is too large. It should be less than 4mb.')

        team = Team.objects.filter(id=team_id).filter().first()
        avatar = f"{settings.TEAM_AVATAR_URL}{team_id}.{file.name.split('.')[-1]}"
        os.makedirs(os.path.dirname(avatar), exist_ok=True)

        for dir_file in os.listdir(os.path.dirname(avatar)):
            if dir_file.startswith(str(team_id)):
                dir_file_path = os.path.join(os.path.dirname(avatar), dir_file)
                if os.path.isfile(dir_file_path):
                    os.remove(dir_file_path)

        with open(avatar, "wb+") as f:
            for chunk in file.chunks():
                f.write(chunk)
        team.avatar = avatar
        team.save()
        return ResponseTemplate(Error.SUCCESS, 'Edit team avatar successfully')
    except Exception as e:
        return ResponseTemplate(Error.FAILED, str(e))
