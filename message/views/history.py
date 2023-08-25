from rest_framework.decorators import api_view

from shared.token import check_token


@api_view(['GET'])
def get_history(request, team_id):
    response, user_id = check_token(request)
    if user_id == -1:
        return response
