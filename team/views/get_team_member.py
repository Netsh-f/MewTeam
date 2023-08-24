from rest_framework.decorators import api_view
from shared.error import Error
from shared.res_temp import ResponseTemplate
from shared.token import get_identity_from_token, verify_token
from team.models import Team, UserTeamShip
from user.models import User


@api_view(['POST'])
def get_team_member(request):
    user_token = request.META.get('HTTP_AUTHORIZATION', '')
    if not verify_token(user_token):
        return ResponseTemplate(Error.TOKEN_INVALID, "token is invalid")
    data = request.data
    team_id = data['team_id']
    user_team_ships = UserTeamShip.objects.filter(team_id=team_id)
    team_members_info = []
    for ship in user_team_ships:
        user = ship.user
        team_members_info.append({
            'id': user.id,
            'nickname': user.nickname,
            'name': user.name,
            'email': user.email,
            'identify': ship.identify,
        })
    return ResponseTemplate(Error.SUCCESS, 'get team member success!', team_members_info)
