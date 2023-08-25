from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from rest_framework.decorators import api_view

from shared.email import send_invitation
from shared.error import Error
from shared.random import generate_invitation_code
from shared.res_temp import ResponseTemplate
from shared.token import check_token
from team.models import UserTeamShip, Team, Invitations
from user.models import User


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
