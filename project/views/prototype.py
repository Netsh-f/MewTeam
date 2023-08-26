"""
============================
# @Time    : 2023/8/26 20:00
# @Author  : Elaikona
# @FileName: prototype.py
===========================
"""

from rest_framework.decorators import api_view

from project.models import Project, Prototype
from project.serializers import PrototypeSerializer
from shared.error import Error
from shared.permission import is_team_member
from shared.res_temp import ResponseTemplate
from shared.token import check_token


@api_view(['POST'])
def save_prototype(request, pro_id):
    try:
        response, user_id = check_token(request)
        if user_id == -1:
            return response
        project = Project.objects.get(id=pro_id)
        if not is_team_member(user_id, project.team_id):
            return ResponseTemplate(Error.PERMISSION_DENIED, 'you are not one member of this team')
        content = request.data['content']
        Prototype.objects.create(project_id=pro_id, content=content)
        return ResponseTemplate(Error.SUCCESS, 'save prototype successfully')
    except Project.DoesNotExist:
        return ResponseTemplate(Error.DATA_NOT_FOUND, 'project not found')
    except Exception as e:
        return ResponseTemplate(Error.FAILED, str(e))


@api_view(['GET'])
def get_latest_prototype(request, pro_id):
    try:
        response, user_id = check_token(request)
        if user_id == -1:
            return response
        project = Project.objects.get(id=pro_id)
        if not is_team_member(user_id, project.team_id):
            return ResponseTemplate(Error.PERMISSION_DENIED, 'you are not one member of this team')
        latest_prototype = Prototype.objects.filter(project_id=pro_id).order_by('-timestamp').first()
        return ResponseTemplate(Error.SUCCESS, 'get latest prototype successfully',
                                data=PrototypeSerializer(latest_prototype).data)
    except Project.DoesNotExist:
        return ResponseTemplate(Error.DATA_NOT_FOUND, 'project not found')
    except Exception as e:
        return ResponseTemplate(Error.FAILED, str(e))
