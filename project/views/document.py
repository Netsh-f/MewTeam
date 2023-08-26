"""
============================
# @Time    : 2023/8/26 16:24
# @Author  : Elaikona
# @FileName: document.py
===========================
"""
from rest_framework.decorators import api_view

from project.models import Document, Project
from project.serializers import DocumentSerializer, DocumentSimpleSerializer
from shared.error import Error
from shared.permission import is_team_member
from shared.res_temp import ResponseTemplate
from shared.token import check_token


@api_view(['POST'])
def save_document(request, pro_id):
    try:
        response, user_id = check_token(request)
        if user_id == -1:
            return response
        project = Project.objects.get(id=pro_id)
        if not is_team_member(user_id, project.team_id):
            return ResponseTemplate(Error.PERMISSION_DENIED, 'you are not one member of this team')
        content = request.data['content']
        Document.objects.create(project_id=pro_id, content=content)
        return ResponseTemplate(Error.SUCCESS, 'save document successfully')
    except Project.DoesNotExist:
        return ResponseTemplate(Error.DATA_NOT_FOUND, 'project not found')
    except Exception as e:
        return ResponseTemplate(Error.FAILED, str(e))


@api_view(['GET'])
def get_latest_document(request, pro_id):
    try:
        response, user_id = check_token(request)
        if user_id == -1:
            return response
        project = Project.objects.get(id=pro_id)
        if not is_team_member(user_id, project.team_id):
            return ResponseTemplate(Error.PERMISSION_DENIED, 'you are not one member of this team')
        latest_document = Document.objects.filter(project_id=pro_id).order_by('-timestamp').first()
        return ResponseTemplate(Error.SUCCESS, 'get latest document successfully',
                                data=DocumentSerializer(latest_document).data)
    except Project.DoesNotExist:
        return ResponseTemplate(Error.DATA_NOT_FOUND, 'project not found')
    except Exception as e:
        return ResponseTemplate(Error.FAILED, str(e))


@api_view(['GET'])
def get_history_document_list(request, pro_id):
    try:
        response, user_id = check_token(request)
        if user_id == -1:
            return response
        project = Project.objects.get(id=pro_id)
        if not is_team_member(user_id, project.team_id):
            return ResponseTemplate(Error.PERMISSION_DENIED, 'you are not one member of this team')
        documents = Document.objects.filter(project_id=pro_id).all().order_by('-timestamp').all()
        return ResponseTemplate(Error.SUCCESS, 'get history documents list successfully',
                                data=DocumentSimpleSerializer(documents, many=True))
    except Project.DoesNotExist:
        return ResponseTemplate(Error.DATA_NOT_FOUND, 'project not found')
    except Exception as e:
        return ResponseTemplate(Error.FAILED, str(e))


@api_view(['GET'])
def get_document_by_id(request, document_id):
    try:
        response, user_id = check_token(request)
        if user_id == -1:
            return response
        document = Document.objects.get(id=document_id)
        if not is_team_member(user_id, document.project.team_id):
            return ResponseTemplate(Error.PERMISSION_DENIED, 'you are not one member of this team')
        return ResponseTemplate(Error.SUCCESS, f'get {document_id} document successfully',
                                data=DocumentSerializer(document).data)
    except Project.DoesNotExist:
        return ResponseTemplate(Error.DATA_NOT_FOUND, 'project not found')
    except Exception as e:
        return ResponseTemplate(Error.FAILED, str(e))
