"""
============================
# @Time    : 2023/8/27 14:34
# @Author  : Elaikona
# @FileName: guest.py
===========================
"""
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.decorators import api_view

from project.models import Document
from shared.error import Error
from shared.guest_token import generate_encrypted_token, check_guest_token
from shared.permission import is_admin_or_creator
from shared.res_temp import ResponseTemplate
from shared.token import check_token


@api_view(['POST'])
def generate_guest_token(request, document_id):
    try:
        response, user_id = check_token(request)
        if user_id == -1:
            return response
        document = Document.objects.get(id=document_id)
        if not is_admin_or_creator(user_id, document.project.team_id):
            return ResponseTemplate(Error.PERMISSION_DENIED, 'you are not the admin or creator of this team')
        data = request.data
        edit_permission = data['edit_permission']
        expiration_days = data['expiration_days']
        token = generate_encrypted_token(document_id, edit_permission, expiration_days)
        return ResponseTemplate(Error.SUCCESS, 'get guest token successfully', data={'token': token})
    except ObjectDoesNotExist as e:
        return ResponseTemplate(Error.DATA_NOT_FOUND, str(e))
    except Exception as e:
        return ResponseTemplate(Error.FAILED, str(e))


@api_view(['GET'])
def validate_guest_token(request):
    try:
        edit_permission, document_id, expiration_date, response = check_guest_token(request)
        if document_id == -1:
            return response
        return ResponseTemplate(Error.SUCCESS, 'valid guest token', data={
            'edit_permission': edit_permission,
            'document_id': document_id,
            'expiration_date': expiration_date,
        })
    except Exception as e:
        return ResponseTemplate(Error.FAILED, str(e))
