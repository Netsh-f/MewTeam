from django.db import transaction
from rest_framework.decorators import api_view
from shared.error import Error
from shared.res_temp import ResponseTemplate
from shared.token import check_token
from team.models import UserTeamShip, Team

