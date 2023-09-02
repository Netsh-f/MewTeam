"""
============================
# @Time    : 2023/8/26 16:24
# @Author  : Elaikona
# @FileName: document.py
===========================
"""
import logging

from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from rest_framework import status
from rest_framework.decorators import api_view

from message.models import Mention
from project.models import Document, Project, DocumentContent
from project.serializers import DocumentContentSerializer, DocumentContentSimpleSerializer, DocumentDirSerializer
from shared.error import Error
from shared.guest_token import check_guest_token
from shared.permission import is_team_member
from shared.res_temp import ResponseTemplate
from shared.token import check_token

logger = logging.getLogger("__name__")

@api_view(['POST'])
def create_document(request, pro_id):
    try:
        response, user_id = check_token(request)
        if user_id == -1:
            return response
        project = Project.objects.get(id=pro_id)
        if not is_team_member(user_id, project.team_id):
            return ResponseTemplate(Error.PERMISSION_DENIED, 'you are not one member of this team')
        name = request.data['name']
        content = request.data['content']
        document = Document.objects.create(project=project, name=name)
        DocumentContent.objects.create(document=document, content=content)  # content is json format
        return ResponseTemplate(Error.SUCCESS, 'create new document successfully')
    except KeyError as keyError:
        return ResponseTemplate(Error.FAILED, 'Invalid or missing key. ' + str(keyError),
                                status=status.HTTP_400_BAD_REQUEST)
    except Project.DoesNotExist:
        return ResponseTemplate(Error.DATA_NOT_FOUND, 'project not found')
    except Exception as e:
        return ResponseTemplate(Error.FAILED, str(e))


@api_view(['POST'])
def save_document(request, document_id):
    try:
        response, current_user_id = check_token(request)
        data, guest_response = check_guest_token(request)
        if current_user_id == -1 and data is None:
            return response
        if data is not None and not data['edit_permission']:
            return ResponseTemplate(Error.PERMISSION_DENIED, 'you can not edit this document')
        document = Document.objects.get(id=document_id)
        if not is_team_member(current_user_id, document.project.team_id):
            return ResponseTemplate(Error.PERMISSION_DENIED, 'you are not one member of this team')
        content = request.data['content']
        at_user_list = request.data['at_user_list']
        auto_save = request.data['auto_save']

        mentions = document.mention_set.all()
        mentioned_list = mentions.values_list('receiver_user_id', flat=True)
        for at_user_id in at_user_list:
            if at_user_id not in mentioned_list:
                Mention.objects.create(sender_user_id=current_user_id, receiver_user_id=at_user_id,
                                       document=document,
                                       type=Mention.MentionType.DOCUMENT)
        for mention in mentions:
            if mention.receiver_user_id not in at_user_list:
                mention.delete()

        DocumentContent.objects.create(document=document, content=content, auto_save=auto_save)
        document.modified_at = timezone.now()
        document.save()
        return ResponseTemplate(Error.SUCCESS, 'save document successfully')
    except KeyError as keyError:
        return ResponseTemplate(Error.FAILED, 'Invalid or missing key. ' + str(keyError),
                                status=status.HTTP_400_BAD_REQUEST)
    except Project.DoesNotExist:
        return ResponseTemplate(Error.DATA_NOT_FOUND, 'project not found')
    except Exception as e:
        return ResponseTemplate(Error.FAILED, str(e))


@api_view(['GET'])
def get_latest_document(request, document_id):
    try:
        response, user_id = check_token(request)
        data, guest_response = check_guest_token(request)
        if user_id == -1 and data is None:
            return response
        document = Document.objects.get(id=document_id)
        if not is_team_member(user_id, document.project.team_id):
            return ResponseTemplate(Error.PERMISSION_DENIED, 'you are not one member of this team')
        latest_document_content = DocumentContent.objects.filter(document=document).order_by('-timestamp').first()
        return ResponseTemplate(Error.SUCCESS, 'get latest document successfully',
                                data=DocumentContentSerializer(latest_document_content).data)
    except KeyError as keyError:
        return ResponseTemplate(Error.FAILED, 'Invalid or missing key. ' + str(keyError),
                                status=status.HTTP_400_BAD_REQUEST)
    except Project.DoesNotExist:
        return ResponseTemplate(Error.DATA_NOT_FOUND, 'project not found')
    except Exception as e:
        return ResponseTemplate(Error.FAILED, str(e))


@api_view(['GET'])
def get_history_document_list(request, document_id):
    try:
        response, user_id = check_token(request)
        if user_id == -1:
            return response
        document = Document.objects.get(id=document_id)
        if not is_team_member(user_id, document.project.team_id):
            return ResponseTemplate(Error.PERMISSION_DENIED, 'you are not one member of this team')
        document_contents = document.documentcontent_set.filter(auto_save=False).order_by('-timestamp').all()
        return ResponseTemplate(Error.SUCCESS, 'get history documents list successfully',
                                data=DocumentContentSimpleSerializer(document_contents, many=True).data)
    except KeyError as keyError:
        return ResponseTemplate(Error.FAILED, 'Invalid or missing key. ' + str(keyError),
                                status=status.HTTP_400_BAD_REQUEST)
    except ObjectDoesNotExist as e:
        return ResponseTemplate(Error.DATA_NOT_FOUND, str(e))
    except Exception as e:
        return ResponseTemplate(Error.FAILED, str(e))


@api_view(['GET'])
def get_document_content_by_id(request, document_content_id):
    try:
        response, user_id = check_token(request)
        if user_id == -1:
            return response
        document_content = DocumentContent.objects.get(id=document_content_id)
        if not is_team_member(user_id, document_content.document.project.team_id):
            return ResponseTemplate(Error.PERMISSION_DENIED, 'you are not one member of this team')
        return ResponseTemplate(Error.SUCCESS, f'get {document_content_id} document history content successfully',
                                data=DocumentContentSerializer(document_content).data)
    except KeyError as keyError:
        return ResponseTemplate(Error.FAILED, 'Invalid or missing key. ' + str(keyError),
                                status=status.HTTP_400_BAD_REQUEST)
    except ObjectDoesNotExist as e:
        return ResponseTemplate(Error.DATA_NOT_FOUND, str(e))
    except Exception as e:
        return ResponseTemplate(Error.FAILED, str(e))


@api_view(['GET'])
def get_documents_by_project_id(request, pro_id):
    try:
        response, user_id = check_token(request)
        if user_id == -1:
            return response
        project = Project.objects.get(id=pro_id)
        documents = project.document_set.all()
        return ResponseTemplate(Error.SUCCESS, DocumentDirSerializer(documents, many=True).data)
    except ObjectDoesNotExist as e:
        return ResponseTemplate(Error.DATA_NOT_FOUND, str(e))
    except Exception as e:
        return ResponseTemplate(Error.FAILED, str(e))


@api_view(['PUT'])
def delete_document(request, document_id):
    try:
        response, user_id = check_token(request)
        if user_id == -1:
            return response
        document = Document.objects.get(id=document_id)
        if not is_team_member(user_id, document.project.team_id):
            return ResponseTemplate(Error.PERMISSION_DENIED, 'you are not one member of this team')
        document.is_deleted = True
        document.save()
        return ResponseTemplate(Error.SUCCESS, 'delete document successfully')
    except ObjectDoesNotExist as e:
        return ResponseTemplate(Error.DATA_NOT_FOUND, str(e))
    except Exception as e:
        return ResponseTemplate(Error.FAILED, str(e))


@api_view(['PUT'])
def restore_document(request, document_id):
    try:
        response, user_id = check_token(request)
        if user_id == -1:
            return response
        document = Document.objects.get(id=document_id)
        if not is_team_member(user_id, document.project.team_id):
            return ResponseTemplate(Error.PERMISSION_DENIED, 'you are not one member of this team')
        document.is_deleted = False
        document.save()
        return ResponseTemplate(Error.SUCCESS, 'restore document successfully')
    except ObjectDoesNotExist as e:
        return ResponseTemplate(Error.DATA_NOT_FOUND, str(e))
    except Exception as e:
        return ResponseTemplate(Error.FAILED, str(e))


@api_view(['DELETE'])
def destroy_document(request, document_id):
    try:
        response, user_id = check_token(request)
        if user_id == -1:
            return response
        document = Document.objects.get(id=document_id)
        if not is_team_member(user_id, document.project.team_id):
            return ResponseTemplate(Error.PERMISSION_DENIED, 'you are not one member of this team')
        document.delete()
        return ResponseTemplate(Error.SUCCESS, 'destroy document successfully')
    except ObjectDoesNotExist as e:
        return ResponseTemplate(Error.DATA_NOT_FOUND, str(e))
    except Exception as e:
        return ResponseTemplate(Error.FAILED, str(e))
