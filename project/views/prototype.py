"""
============================
# @Time    : 2023/8/26 20:00
# @Author  : Elaikona
# @FileName: prototype.py
===========================
"""

from rest_framework.decorators import api_view

from project.models import Project, Prototype, PrototypeContent
from project.serializers import PrototypeSerializer, PrototypeContentSerializer
from shared.error import Error
from shared.permission import is_team_member
from shared.res_temp import ResponseTemplate
from shared.token import check_token

@api_view(['POST'])
def create_prototype(request, pro_id):
    try:
        response, user_id = check_token(request)
        if user_id == -1:
            return response
        project = Project.objects.get(id=pro_id)
        if not is_team_member(user_id, project.team_id):
            return ResponseTemplate(Error.PERMISSION_DENIED, 'you are not one member of this team')
        name = request.data['name']
        if Prototype.objects.filter(project_id=pro_id, name=name).exists():
            return ResponseTemplate(Error.PTT_EXISTS, 'Prototype already exists')
        ptt = Prototype.objects.create(project_id=pro_id, name=name)
        PrototypeContent.objects.create(prototype=ptt)
        return ResponseTemplate(Error.SUCCESS, 'create prototype successfully')
    except Project.DoesNotExist:
        return ResponseTemplate(Error.DATA_NOT_FOUND, 'project not found')
    except Exception as e:
        return ResponseTemplate(Error.FAILED, str(e))

@api_view(['GET'])
def list_prototype(request, pro_id):
    try:
        response, user_id = check_token(request)
        if user_id == -1:
            return response
        project = Project.objects.get(id=pro_id)
        if not is_team_member(user_id, project.team_id):
            return ResponseTemplate(Error.PERMISSION_DENIED, 'you are not one member of this team')
        return ResponseTemplate(Error.SUCCESS, 'query prototypes successfully',
                                data=PrototypeSerializer(Prototype.objects.filter(project_id=pro_id),
                                                         many=True).data)
    except Project.DoesNotExist:
        return ResponseTemplate(Error.DATA_NOT_FOUND, 'project not found')
    except Exception as e:
        return ResponseTemplate(Error.FAILED, str(e))
@api_view(['PUT'])
def update_prototype(request, ptt_id):
    try:
        response, user_id = check_token(request)
        if user_id == -1:
            return response
        name = request.data['name']
        ptt = Prototype.objects.filter(id=ptt_id)
        if not ptt.exists():
            return ResponseTemplate(Error.PTT_NOT_EXISTS, 'Prototype does not exist')
        ptt.update(name=name)
        return ResponseTemplate(Error.SUCCESS, 'update prototype successfully')
    except Exception as e:
        return ResponseTemplate(Error.FAILED, str(e))

@api_view(['DELETE'])
def delete_prototype(request, ptt_id):
    try:
        response, user_id = check_token(request)
        if user_id == -1:
            return response
        ptt = Prototype.objects.filter(id=ptt_id)
        if not ptt.exists():
            return ResponseTemplate(Error.PTT_NOT_EXISTS, 'Prototype does not exist')
        ptt.delete()
        return ResponseTemplate(Error.SUCCESS, 'delete prototype successfully')
    except Exception as e:
        return ResponseTemplate(Error.FAILED, str(e))

@api_view(['POST'])
def save_prototype(request, ptt_id):
    try:
        response, user_id = check_token(request)
        if user_id == -1:
            return response
        content = request.data['content']
        ptt = Prototype.objects.get(id=ptt_id)
        PrototypeContent.objects.create(prototype=ptt, content=content)
        return ResponseTemplate(Error.SUCCESS, 'save prototype successfully')
    except Prototype.DoesNotExist:
        return ResponseTemplate(Error.DATA_NOT_FOUND, 'prototype not found')
    except Exception as e:
        return ResponseTemplate(Error.FAILED, str(e))

@api_view(['GET'])
def get_latest_prototype(request, ptt_id):
    try:
        response, user_id = check_token(request)
        if user_id == -1:
            return response
        latest_prototype = PrototypeContent.objects.filter(prototype_id=ptt_id).\
                            order_by('-timestamp').first()
        return ResponseTemplate(Error.SUCCESS, 'get latest prototype successfully',
                                data=PrototypeContentSerializer(latest_prototype).data)
    except Project.DoesNotExist:
        return ResponseTemplate(Error.DATA_NOT_FOUND, 'project not found')
    except Exception as e:
        return ResponseTemplate(Error.FAILED, str(e))
