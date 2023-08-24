from django.db import transaction
from rest_framework.decorators import api_view
from shared.error import Error
from shared.res_temp import ResponseTemplate
from shared.token import check_token
from team.models import UserTeamShip, Team


@api_view(['POST'])
def create_team(request):
    response, user_id = check_token(request)
    if user_id == -1:
        return response
    data = request.data
    name = data['name']
    try:
        with transaction.atomic():
            new_team = Team.objects.create(name=name)
            UserTeamShip.objects.create(user_id=user_id, team=new_team, identify=UserTeamShip.Identify.CREATOR)
            return ResponseTemplate(Error.SUCCESS, 'Team created successfully!')
    except Exception as e:
        return ResponseTemplate(Error.DATABASE_INTERNAL_ERROR, str(e))


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


def _is_admin(user_id, team_id):
    try:
        ship = UserTeamShip.objects.get(user_id=user_id, team_id=team_id)
        return ship.identify in [UserTeamShip.Identify.ADMIN, UserTeamShip.Identify.CREATOR]
    except UserTeamShip.DoesNotExist:
        return False


def _is_normal(user_id, team_id):
    try:
        ship = UserTeamShip.objects.get(user_id=user_id, team_id=team_id)
        return ship.identify == UserTeamShip.Identify.NORMAL
    except UserTeamShip.DoesNotExist:
        return False


@api_view(['PUT'])
def promote_user_to_admin(request, team_id, user_id):
    response, current_user_id = check_token(request)
    if current_user_id == -1:
        return response
    if not _is_admin(current_user_id, team_id):
        return ResponseTemplate(Error.PERMISSION_DENIED, 'The current user is not a admin in this team')
    if not _is_normal(user_id, team_id):
        return ResponseTemplate(Error.IDENTIFY_ERROR, 'This user is not a normal member in this team')
    try:
        ship = UserTeamShip.objects.get(user_id=user_id, team_id=team_id)
        ship.identify = UserTeamShip.Identify.ADMIN
        ship.save()
    except UserTeamShip.DoesNotExist:
        return ResponseTemplate(Error.DATA_NOT_FOUND, 'User, team or relationship not found')
    except Exception as e:
        return ResponseTemplate(Error.DATABASE_INTERNAL_ERROR, str(e))
