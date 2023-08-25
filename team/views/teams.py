import logging

from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from rest_framework import status
from rest_framework.decorators import api_view

from MewTeam.settings import SECRETS
from shared.email import send_invitation
from shared.error import Error
from shared.random import generate_invitation_code
from shared.res_temp import ResponseTemplate
from shared.token import check_token
from team.models import UserTeamShip, Team, Invitations
from user.models import User

logger = logging.getLogger(__name__)


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
            return ResponseTemplate(Error.SUCCESS, 'Team created successfully!', data={'team_id': new_team.id})
    except Exception as e:
        return ResponseTemplate(Error.DATABASE_INTERNAL_ERROR, str(e) + "user_id=" + str(user_id))


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


def _is_admin_or_creator(user_id, team_id):
    try:
        ship = UserTeamShip.objects.get(user_id=user_id, team_id=team_id)
        return ship.identify in [UserTeamShip.Identify.ADMIN, UserTeamShip.Identify.CREATOR]
    except UserTeamShip.DoesNotExist:
        return False


def _is_creator(user_id, team_id):
    try:
        ship = UserTeamShip.objects.get(user_id=user_id, team_id=team_id)
        return ship.identify == UserTeamShip.Identify.CREATOR
    except UserTeamShip.DoesNotExist:
        return False


def _is_admin(user_id, team_id):
    try:
        ship = UserTeamShip.objects.get(user_id=user_id, team_id=team_id)
        return ship.identify == UserTeamShip.Identify.ADMIN
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
    if not _is_admin_or_creator(current_user_id, team_id):
        return ResponseTemplate(Error.PERMISSION_DENIED, 'The current user is not a admin or creator in this team')
    if not _is_normal(user_id, team_id):
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
    if not _is_admin_or_creator(current_user_id, team_id):
        return ResponseTemplate(Error.PERMISSION_DENIED, 'The current user is not a admin or creator in this team')
    if not _is_admin(user_id, team_id):
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


@api_view(['POST'])
def generate_invitation(request, team_id):
    response, current_user_id = check_token(request)
    if current_user_id == -1:
        return response
    try:
        email_addr = request.data['email']
        team = Team.objects.get(id=team_id)
        sender = User.objects.get(id=current_user_id)
        invitation_code = generate_invitation_code()
        invitation = Invitations(team=team, sender=sender, invitation_code=invitation_code, receiver_email=email_addr)
        invitation.save()
        send_invitation(invitation)
        return ResponseTemplate(Error.SUCCESS, 'send invitation successfully')
    except KeyError:
        return ResponseTemplate(Error.FAILED, 'Invalid key', status=status.HTTP_400_BAD_REQUEST)
    except Team.DoesNotExist:
        return ResponseTemplate(Error.TEAM_NOT_EXISTS, 'team not exists')
    except User.DoesNotExist:
        return ResponseTemplate(Error.USER_NOT_EXISTS, 'user not exists')
    except Exception as e:
        return ResponseTemplate(Error.DATABASE_INTERNAL_ERROR, str(e))


@api_view(['GET'])
def get_team_list(request):
    response, current_user_id = check_token(request)
    if current_user_id == -1:
        return response
    try:
        ships = UserTeamShip.objects.filter(user_id=current_user_id)
        team_list = []
        for ship in ships:
            team_list.append({
                'team_id': ship.team.id,
                'name': ship.team.name
            })
        return ResponseTemplate(Error.SUCCESS, 'get current user team list successfully', data=team_list)
    except ObjectDoesNotExist as e:
        return ResponseTemplate(Error.DATABASE_INTERNAL_ERROR, str(e))
    except Exception as e:
        return ResponseTemplate(Error.FAILED, str(e))


@api_view(['DELETE'])
def remove_team_user(request, team_id, user_id):
    response, current_user_id = check_token(request)
    if current_user_id == -1:
        return response
    if not _is_admin_or_creator(current_user_id, team_id):
        return ResponseTemplate(Error.PERMISSION_DENIED, 'The current user is not a admin or creator in this team.')
    if _is_admin_or_creator(user_id):
        return ResponseTemplate(Error.IDENTIFY_ERROR, 'This user to be removed is the admin or creator in this team.')
    try:
        ship = UserTeamShip.objects.get(user_id=user_id, team_id=team_id)
        ship.delete()
        return ResponseTemplate(Error.SUCCESS, 'remove this user from team successfully')
    except ObjectDoesNotExist as e:
        return ResponseTemplate(Error.DATABASE_INTERNAL_ERROR, str(e))
    except Exception as e:
        return ResponseTemplate(Error.FAILED, str(e))


@api_view(['POST'])
def join_team_with_invitation(request):
    response, current_user_id = check_token(request)
    if current_user_id == -1:
        return response
    try:
        invitation_code = request.data['invitation_code']
        invitation = Invitations.objects.filter(invitation_code=invitation_code).first()
        if not invitation:
            return ResponseTemplate(Error.INVALID_INVITATION_CODE, 'Invalid invitation code')
        user = User.objects.get(id=current_user_id)
        team = invitation.team
        UserTeamShip.objects.create(user=user, team=team)
        return ResponseTemplate(Error.SUCCESS, 'join team successfully')
    except ObjectDoesNotExist as e:
        return ResponseTemplate(Error.DATABASE_INTERNAL_ERROR, str(e))
    except Exception as e:
        return ResponseTemplate(Error.FAILED, str(e))


@api_view(['DELETE'])
def disband_team(request, team_id):
    response, current_user_id = check_token(request)
    if current_user_id == -1:
        return response
    try:
        team = Team.objects.get(id=team_id)
        if not _is_creator(current_user_id, team_id):
            return ResponseTemplate(Error.PERMISSION_DENIED, 'you are not the creator of the team')
        team.delete()
        return ResponseTemplate(Error.SUCCESS, 'Team disbanded successfully')
    except Exception as e:
        return ResponseTemplate(Error.FAILED, str(e))
