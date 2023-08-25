from django.core.exceptions import ObjectDoesNotExist
from rest_framework.decorators import api_view

from shared.error import Error
from shared.res_temp import ResponseTemplate
from shared.token import check_token
from team.models import UserTeamShip
from team.views.utils.permission import is_admin_or_creator, is_normal, is_admin


@api_view(['GET'])
def get_team_user_list(request, team_id):
    response, user_id = check_token(request)
    if user_id == -1:
        return response
    try:
        UserTeamShip.objects.get(user_id=user_id, team_id=team_id)
    except UserTeamShip.DoesNotExist:
        return ResponseTemplate(Error.PERMISSION_DENIED, "You are not a member of this team")

    user_team_ships = UserTeamShip.objects.filter(team_id=team_id)
    team_user_list = []
    for ship in user_team_ships:
        user = ship.user
        team_user_list.append({
            'id': user.id,
            'nickname': user.nickname,
            'name': user.name,
            'email': user.email,
            'identify': ship.identify,
        })
    return ResponseTemplate(Error.SUCCESS, 'get team member success!', data=team_user_list)


@api_view(['PUT'])
def promote_user_to_admin(request, team_id, user_id):
    response, current_user_id = check_token(request)
    if current_user_id == -1:
        return response
    if not is_admin_or_creator(current_user_id, team_id):
        return ResponseTemplate(Error.PERMISSION_DENIED, 'The current user is not a admin or creator in this team')
    if not is_normal(user_id, team_id):
        return ResponseTemplate(Error.IDENTIFY_ERROR, 'This user is not a normal member in this team')
    try:
        ship = UserTeamShip.objects.get(user_id=user_id, team_id=team_id)
        ship.identify = UserTeamShip.Identify.ADMIN
        ship.save()
        return ResponseTemplate(Error.SUCCESS, 'promote successfully')
    except UserTeamShip.DoesNotExist:
        return ResponseTemplate(Error.DATA_NOT_FOUND, 'User, team or relationship not found')
    except Exception as e:
        return ResponseTemplate(Error.DATABASE_INTERNAL_ERROR, str(e))


@api_view(['PUT'])
def demote_admin_to_user(request, team_id, user_id):
    response, current_user_id = check_token(request)
    if current_user_id == -1:
        return response
    if not is_admin_or_creator(current_user_id, team_id):
        return ResponseTemplate(Error.PERMISSION_DENIED, 'The current user is not a admin or creator in this team')
    if not is_admin(user_id, team_id):
        return ResponseTemplate(Error.IDENTIFY_ERROR, 'This user is not a admin member in this team')
    try:
        ship = UserTeamShip.objects.get(user_id=user_id, team_id=team_id)
        ship.identify = UserTeamShip.Identify.NORMAL
        ship.save()
        return ResponseTemplate(Error.SUCCESS, 'demote successfully')
    except UserTeamShip.DoesNotExist:
        return ResponseTemplate(Error.DATA_NOT_FOUND, 'User, team or relationship not found')
    except Exception as e:
        return ResponseTemplate(Error.DATABASE_INTERNAL_ERROR, str(e))


@api_view(['DELETE'])
def remove_team_user(request, team_id, user_id):
    response, current_user_id = check_token(request)
    if current_user_id == -1:
        return response
    if not is_admin_or_creator(current_user_id, team_id):
        return ResponseTemplate(Error.PERMISSION_DENIED, 'The current user is not a admin or creator in this team.')
    if is_admin_or_creator(user_id, team_id):
        return ResponseTemplate(Error.IDENTIFY_ERROR, 'This user to be removed is the admin or creator in this team.')
    try:
        ship = UserTeamShip.objects.get(user_id=user_id, team_id=team_id)
        ship.delete()
        return ResponseTemplate(Error.SUCCESS, 'remove this user from team successfully')
    except ObjectDoesNotExist as e:
        return ResponseTemplate(Error.DATABASE_INTERNAL_ERROR, str(e))
    except Exception as e:
        return ResponseTemplate(Error.FAILED, str(e))
