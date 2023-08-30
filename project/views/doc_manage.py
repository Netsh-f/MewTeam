# ------- Litang Save The World! -------
#
# @Time    : 2023/8/30 10:17
# @Author  : Lynx
# @File    : doc_manage.py
#
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from rest_framework.decorators import api_view

from project.models import Project, Document, DocumentContent, DocumentDir
from project.serializers import DocumentSerializer
from project.views.utils._doc_manage import _init_doc_struction
from shared.error import Error
from shared.permission import is_team_member
from shared.res_temp import ResponseTemplate
from shared.token import check_token


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
        dir_name = request.data['dir_name']
        root_dir = DocumentDir.objects.filter(project=project, name=f'root_{pro_id}')
        if not root_dir.exists():
            return ResponseTemplate(Error.DOC_STRUCT_NOT_INIT, 'Project structure not initialized')

        root_dir = root_dir.first()
        if dir_name == root_dir.name:
            document = Document.objects.create(project=project, name=name, par_dir=root_dir)
        else:
            sub_dir = DocumentDir.objects.filter(name=name, par_dir=root_dir)
            if not sub_dir.exists():
                return ResponseTemplate(Error.DOC_DIR_NOT_EXISTS, 'Document subdirectory does not exist')
            document = Document.objects.create(project=project, name=name, par_dir=sub_dir.first())
        DocumentContent.objects.create(document=document, content=content)  # content is json format
        return ResponseTemplate(Error.SUCCESS, 'create new document successfully')
    except KeyError as keyError:
        return ResponseTemplate(Error.FAILED, 'Invalid or missing key. ' + str(keyError),
                                status=status.HTTP_400_BAD_REQUEST)
    except Project.DoesNotExist:
        return ResponseTemplate(Error.DATA_NOT_FOUND, 'project not found')
    except Exception as e:
        return ResponseTemplate(Error.FAILED, str(e))

@api_view(['GET'])
def get_documents(request, pro_id):
    try:
        response, user_id = check_token(request)
        if user_id == -1:
            return response
        project = Project.objects.get(id=pro_id)
        if not is_team_member(user_id, project.team_id):
            return ResponseTemplate(Error.PERMISSION_DENIED, 'you are not one member of this team')

        _init_doc_struction(project)
        root_dir = DocumentDir.objects.get(name=f'root_{project.id}')
        sub_dirs = DocumentDir.objects.filter(par_dir=root_dir)

        sub_dir_list = []
        for sub_dir in sub_dirs:
            sub_dir_list.append({
                'name': sub_dir.name,
                'projects': DocumentSerializer(Document.objects.filter(par_dir=sub_dir)).data
            })
        data = DocumentSerializer(Document.objects.filter(par_dir=root_dir)).data.append(sub_dir_list)
        # documents = project.document_set.all()
        # return ResponseTemplate(Error.SUCCESS, DocumentSerializer(documents, many=True).data)
        return ResponseTemplate(Error.SUCCESS, 'Query Successful', data=data)
    except ObjectDoesNotExist as e:
        return ResponseTemplate(Error.DATA_NOT_FOUND, str(e))
    except Exception as e:
        return ResponseTemplate(Error.FAILED, str(e))

@api_view(['POST'])
def create_dir(request, pro_id):
    try:
        response, user_id = check_token(request)
        if user_id == -1:
            return response
        project = Project.objects.get(id=pro_id)
        if not is_team_member(user_id, project.team_id):
            return ResponseTemplate(Error.PERMISSION_DENIED, 'you are not one member of this team')

        dir_name = request.data['dir_name']
        doc_dirs = DocumentDir.objects.filter(project=project)
        if not doc_dirs.filter(name=f'root_{pro_id}').exists():
            return ResponseTemplate(Error.DOC_STRUCT_NOT_INIT, 'Project structure not initialized')
        if doc_dirs.filter(name=dir_name).exists():
            return ResponseTemplate(Error.DOC_DIR_EXISTS, 'Directory name already exists')
        DocumentDir.objects.create(project=project, name=dir_name)
    except KeyError as keyError:
        return ResponseTemplate(Error.FAILED, 'Invalid or missing key. ' + str(keyError),
                                status=status.HTTP_400_BAD_REQUEST)
    except Project.DoesNotExist:
        return ResponseTemplate(Error.DATA_NOT_FOUND, 'project not found')
    except Exception as e:
        return ResponseTemplate(Error.FAILED, str(e))