"""
============================
# @Time    : 2023/8/26 14:40
# @Author  : Elaikona
# @FileName: chat.py
===========================
"""
import os

from rest_framework.decorators import api_view

from MewTeam import settings
from message.models import MessageFile
from shared.error import Error
from shared.res_temp import ResponseTemplate
from shared.token import check_token


@api_view(['POST'])
def upload_message_file(request):
    try:
        response, user_id = check_token(request)
        if user_id == -1:
            return response
        mid = request.POST.get("mid")
        file = request.FILES.get('file')
        if file is None:
            return ResponseTemplate(Error.FILE_MISSING, 'Missing image file')
        if file.size > settings.MAX_MESSAGE_FILE_SIZE:
            return ResponseTemplate(Error.FILE_SIZE_ILLEGAL, 'Size of file is too large. It should be less than 64mb.')
        filepath = f"{settings.MESSAGE_ROOT}/{mid}/{file.name}"
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, "wb+") as f:
            for chunk in file.chunks():
                f.write(chunk)
        return ResponseTemplate(Error.SUCCESS, 'upload file successfully')
    except Exception as e:
        return ResponseTemplate(Error.FAILED, str(e))
