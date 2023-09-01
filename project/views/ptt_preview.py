# ------- Litang Save The World! -------
#
# @Time    : 2023/9/1 13:42
# @Author  : Lynx
# @File    : ptt_preview.py
#
from rest_framework.decorators import api_view

from project.models import Project
from shared.error import Error
from shared.permission import is_team_member
from shared.random import generate_invitation_code
from shared.res_temp import ResponseTemplate
from shared.token import check_token


@api_view(['GET'])
def generate_ptt_invitation_code(request, pro_id):
    try:
        response, user_id = check_token(request)
        if user_id == -1:
            return response
        project = Project.objects.get(id=pro_id)
        if not is_team_member(user_id, project.team_id):
            return ResponseTemplate(Error.PERMISSION_DENIED, 'you are not one member of this team')

        project.preview_enabled = True
        project.inv_code = generate_invitation_code()
        project.save()
        return ResponseTemplate(Error.SUCCESS, 'Generating success!', project.inv_code)
    except Project.DoesNotExist:
        return ResponseTemplate(Error.DATA_NOT_FOUND, 'project not found')
    except Exception as e:
        return ResponseTemplate(Error.FAILED, str(e))

@api_view(['GET'])
def verify_ptt_invitation_code(request, pro_id):
    try:
        project = Project.objects.get(id=pro_id)
        inv_code = request.GET.get('inv_code')
        if (not project.preview_enabled) or project.inv_code != inv_code:
            return ResponseTemplate(Error.PERMISSION_DENIED, 'Permission denied!')
        else:
            return ResponseTemplate(Error.SUCCESS, 'Preview success!')
    except Project.DoesNotExist:
        return ResponseTemplate(Error.DATA_NOT_FOUND, 'project not found')
    except Exception as e:
        return ResponseTemplate(Error.FAILED, str(e))

@api_view(['DELETE'])
def disable_ptt_preview(request, pro_id):
    try:
        response, user_id = check_token(request)
        if user_id == -1:
            return response
        project = Project.objects.get(id=pro_id)
        if not is_team_member(user_id, project.team_id):
            return ResponseTemplate(Error.PERMISSION_DENIED, 'you are not one member of this team')

        project.preview_enabled = False
        return ResponseTemplate(Error.SUCCESS, 'Preview disabled')
    except Project.DoesNotExist:
        return ResponseTemplate(Error.DATA_NOT_FOUND, 'project not found')
    except Exception as e:
        return ResponseTemplate(Error.FAILED, str(e))