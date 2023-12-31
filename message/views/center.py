import logging

from rest_framework.decorators import api_view

from message.models import Mention
from message.serializers import MentionSerializer
from shared.error import Error
from shared.res_temp import ResponseTemplate
from shared.token import check_token
from user.models import User


@api_view(['GET'])
def get_mentions(request):
    try:
        response, user_id = check_token(request)
        if user_id == -1:
            return response
        mentions = Mention.objects.filter(receiver_user_id=user_id, receiver_deleted=False)
        return ResponseTemplate(Error.SUCCESS, 'get mentions successfully',
                                data=MentionSerializer(mentions, many=True).data)
    except Exception as e:
        return ResponseTemplate(Error.FAILED, str(e))


@api_view(['PUT'])
def set_mention_checked(request, mention_id):
    try:
        response, user_id = check_token(request)
        if user_id == -1:
            return response
        mention = Mention.objects.get(id=mention_id)
        if user_id != mention.receiver_user_id:
            return ResponseTemplate(Error.PERMISSION_DENIED, 'This is not your mention')
        mention.checked = True
        mention.save()
        return ResponseTemplate(Error.SUCCESS, 'set mention checked successfully')
    except Exception as e:
        return ResponseTemplate(Error.SUCCESS, str(e))


@api_view(['PUT'])
def set_all_message_mention_checked(request):
    try:
        response, user_id = check_token(request)
        if user_id == -1:
            return response
        user = User.objects.get(id=user_id)
        mentions = user.received_mention.filter(type=Mention.MentionType.MESSAGE).all()
        for mention in mentions:
            mention.checked = True
            mention.save()
        return ResponseTemplate(Error.SUCCESS, 'set all mentions checked successfully')
    except Exception as e:
        return ResponseTemplate(Error.SUCCESS, str(e))


@api_view(['PUT'])
def set_all_document_mention_checked(request):
    try:
        response, user_id = check_token(request)
        if user_id == -1:
            return response
        user = User.objects.get(id=user_id)
        mentions = user.received_mention.filter(type=Mention.MentionType.DOCUMENT).all()
        for mention in mentions:
            mention.checked = True
            mention.save()
        return ResponseTemplate(Error.SUCCESS, 'set all mentions checked successfully')
    except Exception as e:
        return ResponseTemplate(Error.SUCCESS, str(e))


@api_view(['PUT'])
def set_mention_deleted(request, mention_id):
    try:
        response, user_id = check_token(request)
        if user_id == -1:
            return response
        mention = Mention.objects.get(id=mention_id)
        if user_id != mention.receiver_user_id:
            return ResponseTemplate(Error.PERMISSION_DENIED, 'This is not your mention')
        mention.receiver_deleted = True
        mention.save()
        return ResponseTemplate(Error.SUCCESS, 'set mention deleted successfully')
    except Exception as e:
        return ResponseTemplate(Error.SUCCESS, str(e))


@api_view(['PUT'])
def set_all_message_read_mention_deleted(request):
    try:
        response, user_id = check_token(request)
        if user_id == -1:
            return response
        user = User.objects.get(id=user_id)
        mentions = user.received_mention.filter(type=Mention.MentionType.MESSAGE, checked=True).all()
        for mention in mentions:
            mention.receiver_deleted = True
            mention.save()
        return ResponseTemplate(Error.SUCCESS, 'set all messages read mentions deleted successfully')
    except Exception as e:
        return ResponseTemplate(Error.FAILED, str(e))


@api_view(['PUT'])
def set_all_document_read_mention_deleted(request):
    try:
        response, user_id = check_token(request)
        if user_id == -1:
            return response
        user = User.objects.get(id=user_id)
        mentions = user.received_mention.filter(type=Mention.MentionType.DOCUMENT, checked=True).all()
        for mention in mentions:
            mention.receiver_deleted = True
            mention.save()
        return ResponseTemplate(Error.SUCCESS, 'set all documents read mentions deleted successfully')
    except Exception as e:
        return ResponseTemplate(Error.SUCCESS, str(e))
