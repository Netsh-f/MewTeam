from rest_framework.decorators import api_view
from shared.error import Error
from shared.res_temp import ResponseTemplate
from shared.token import get_identity_from_token, verify_token


@api_view(['POST'])
def get_team_member(request):
    user_token = request.META.get('HTTP_AUTHORIZATION', '')
    if verify_token(user_token):
        user_id = get_identity_from_token(user_token)
    else:
        return ResponseTemplate(Error.TOKEN_INVALID, "token is invalid")
