from team.models import UserTeamShip


def is_admin_or_creator(user_id, team_id):
    try:
        ship = UserTeamShip.objects.get(user_id=user_id, team_id=team_id)
        return ship.identify in [UserTeamShip.Identify.ADMIN, UserTeamShip.Identify.CREATOR]
    except UserTeamShip.DoesNotExist:
        return False


def is_creator(user_id, team_id):
    try:
        ship = UserTeamShip.objects.get(user_id=user_id, team_id=team_id)
        return ship.identify == UserTeamShip.Identify.CREATOR
    except UserTeamShip.DoesNotExist:
        return False


def is_admin(user_id, team_id):
    try:
        ship = UserTeamShip.objects.get(user_id=user_id, team_id=team_id)
        return ship.identify == UserTeamShip.Identify.ADMIN
    except UserTeamShip.DoesNotExist:
        return False


def is_normal(user_id, team_id):
    try:
        ship = UserTeamShip.objects.get(user_id=user_id, team_id=team_id)
        return ship.identify == UserTeamShip.Identify.NORMAL
    except UserTeamShip.DoesNotExist:
        return False
