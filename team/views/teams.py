from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from rest_framework.decorators import api_view

from shared.error import Error
from shared.res_temp import ResponseTemplate
from shared.token import check_token
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
