from rest_framework.decorators import api_view
from shared.error import Error
from shared.res_temp import ResponseTemplate
from shared.token import get_identity_from_token, verify_token
from team.models import Team, UserTeamShip
from user.models import User


@api_view(['POST'])
def get_team_member(request):
    user_token = request.META.get('HTTP_AUTHORIZATION', '')
    if verify_token(user_token):
        user_id = get_identity_from_token(user_token)
    else:
        return ResponseTemplate(Error.TOKEN_INVALID, "token is invalid")
    data = request.data
    team_id = data['team_id']
    user_team_ships = UserTeamShip.objects.filter(team_id=team_id)
    team_members = [user_team_ship.user for user_team_ship in user_team_ships]
    team_members_info = []
    for user in team_members:
        pass
