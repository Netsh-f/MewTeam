# ------- Litang Save The World! -------
#
# @Time    : 2023/8/25 16:30
# @Author  : Lynx
# @File    : safety_check.py
#
from team.models import Team, UserTeamShip
from user.models import User

def _is_legal_identity(user_id: int, team_id: int):
    if User.objects.filter(id=user_id) == None:
        return False
    if Team.objects.filter(id=team_id) == None:
        return False
    if UserTeamShip.objects.filter(user_id=user_id, team_id=team_id) == None:
        return False
    return True