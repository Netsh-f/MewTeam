from rest_framework.decorators import api_view

from message.models import Message
from message.serializers import MessageSerializer
from shared.error import Error
from shared.permission import is_team_member
from shared.res_temp import ResponseTemplate
from shared.token import check_token


@api_view(['GET'])
def get_history(request, team_id):
    try:
        response, user_id = check_token(request)
        if user_id == -1:
            return response
        if not is_team_member(user_id, team_id):
            return ResponseTemplate(Error.PERMISSION_DENIED, 'you are not a member of this team')
        history_messages = Message.objects.filter(team_id=team_id).order_by('-timestamp')[:100]
        serializer = MessageSerializer(history_messages, many=True)
        return ResponseTemplate(Error.SUCCESS, 'get history messages successfully', data=serializer)
    except Exception as e:
        return ResponseTemplate(Error.FAILED, str(e))
