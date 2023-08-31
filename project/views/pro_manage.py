# ------- Litang Save The World! -------
#
# @Time    : 2023/8/25 16:29
# @Author  : Lynx
# @File    : pro_manage.py
#
from datetime import timedelta, datetime

from rest_framework.decorators import api_view

from project.models import Project, Prototype, Document, PrototypeContent, DocumentDir
from project.serializers import ProjectSerializer
from project.views.utils._doc_manage import _init_doc_struction
from project.views.utils.safety_check import _is_legal_identity
from shared.error import Error
from shared.res_temp import ResponseTemplate
from shared.token import check_token


@api_view(['POST'])
def create_project(request, team_id):
    try:
        response, user_id = check_token(request)
        if user_id == -1:
            return response
        data = request.data
        name = data['name']
        cover = data['cover']
        if not _is_legal_identity(user_id, team_id):
            return ResponseTemplate(Error.ILLEGAL_IDENTITY, '非法创建，请检查您的用户状态和团队信息')

        project = Project.objects.filter(team_id=team_id, name=name).first()
        if project:
            return ResponseTemplate(Error.PRO_NAME_EXISTS, '项目名重复')

        new_project = Project(team_id=team_id, name=name, cover=cover)
        new_project.save()
        return ResponseTemplate(Error.SUCCESS, '创建成功！', data=ProjectSerializer(new_project).data)
    except Exception as e:
        return ResponseTemplate(Error.FAILED, str(e))


@api_view(['PUT'])
def update_project(request, pro_id):
    try:
        response, user_id = check_token(request)
        if user_id == -1:
            return response
        data = request.data
        name = data['name']

        project = Project.objects.filter(id=pro_id, is_deleted=False).first()
        if project == None:
            return ResponseTemplate(Error.PRO_NOT_FOUND, '项目不存在')

        if Project.objects.filter(name=name):
            return ResponseTemplate(Error.PRO_NAME_EXISTS, '项目名重复')
        project.name = name
        project.save()
        return ResponseTemplate(Error.SUCCESS, '修改成功！')
    except Exception as e:
        return ResponseTemplate(Error.FAILED, str(e))


@api_view(['DELETE'])
def delete_project(request, pro_id):
    try:
        response, user_id = check_token(request)
        if user_id == -1:
            return response

        project = Project.objects.filter(id=pro_id, is_deleted=False).first()
        if project == None:
            return ResponseTemplate(Error.PRO_NOT_FOUND, '项目不存在')
        project.is_deleted = True
        project.delete_time = datetime.now()
        project.save()
        return ResponseTemplate(Error.SUCCESS, '删除成功！')
    except Exception as e:
        return ResponseTemplate(Error.FAILED, str(e))


@api_view(['POST'])
def recover_project(request, pro_id):
    try:
        response, user_id = check_token(request)
        if user_id == -1:
            return response

        project = Project.objects.filter(id=pro_id, is_deleted=True).first()
        if project == None:
            return ResponseTemplate(Error.PRO_NOT_FOUND, '项目不存在')
        project.is_deleted = False
        project.save()
        return ResponseTemplate(Error.SUCCESS, '恢复成功！', ProjectSerializer(project).data)
    except Exception as e:
        return ResponseTemplate(Error.FAILED, str(e))


@api_view(['GET'])
def list_project(request, team_id):
    try:
        response, user_id = check_token(request)
        if user_id == -1:
            return response
        if not _is_legal_identity(user_id, team_id):
            return ResponseTemplate(Error.ILLEGAL_IDENTITY, '非法列举，请检查您的用户状态和团队信息')

        thirty_days_ago = datetime.now() - timedelta(days=30)
        Project.objects.filter(is_deleted=True, delete_time__lt=thirty_days_ago).delete()
        projects = Project.objects.filter(team_id=team_id).all()

        return ResponseTemplate(Error.SUCCESS, '项目列表获取成功!', data=ProjectSerializer(projects, many=True).data)
    except Exception as e:
        return ResponseTemplate(Error.FAILED, str(e))


@api_view(['DELETE'])
def destroy_project(request, pro_id):
    try:
        response, user_id = check_token(request)
        if user_id == -1:
            return response

        project = Project.objects.filter(id=pro_id, is_deleted=True).first()
        if project == None:
            return ResponseTemplate(Error.PRO_NOT_FOUND, '项目不存在')
        project.delete()
        return ResponseTemplate(Error.SUCCESS, '清空成功！')
    except Exception as e:
        return ResponseTemplate(Error.FAILED, str(e))


@api_view(['DELETE'])
def destroy_all_project(request, team_id):
    try:
        response, user_id = check_token(request)
        if user_id == -1:
            return response
        if not _is_legal_identity(user_id, team_id):
            return ResponseTemplate(Error.ILLEGAL_IDENTITY, '非法清空，请检查您的用户状态和团队信息')

        Project.objects.filter(team_id=team_id, is_deleted=True).delete()
        return ResponseTemplate(Error.SUCCESS, '清空成功！')
    except Exception as e:
        return ResponseTemplate(Error.FAILED, str(e))

@api_view(['GET'])
def search_project(request, team_id):
    try:
        print('------step here')
        response, user_id = check_token(request)
        if user_id == -1:
            return response
        if not _is_legal_identity(user_id, team_id):
            return ResponseTemplate(Error.ILLEGAL_IDENTITY, '非法搜索，请检查您的用户状态和团队信息')

        name = request.data['name']
        projects = Project.objects.filter(team_id=team_id, is_deleted=False, name__icontains=name)
        return ResponseTemplate(Error.SUCCESS, 'Searching success!',
                                ProjectSerializer(projects, many=True).data)

    except KeyError as keyError:
        return ResponseTemplate(Error.FAILED, 'Invalid or missing key')

    except Exception as e:
        return ResponseTemplate(Error.FAILED, str(e))

@api_view(['POST'])
def copy_project(request, pro_id):
    try:
        print('-------step here-------')
        response, user_id = check_token(request)
        if user_id == -1:
            return response

        project = Project.objects.get(id=pro_id, is_deleted=False)
        existing_copies = Project.objects.filter(team_id=project.team_id,
                                                 name__startswith=f'{project.name}_副本')
        existing_copy_numbers = [int(name.split('_副本')[-1]) for name in
                                 existing_copies.values_list('name', flat=True)]
        next_copy_number = max(existing_copy_numbers, default=0) + 1
        new_copy_name = f'{project.name}_副本{next_copy_number}'
        pro_copy = Project.objects.create(name=new_copy_name, cover=project.cover, team_id=project.team_id)

        # ptt copy
        ptts = Prototype.objects.filter(project=project)
        for ptt in ptts:
            ptt_copy = Prototype.objects.create(name=ptt.name, project=pro_copy)
            pttcont = PrototypeContent.objects.filter(prototype=ptt).\
                order_by('-timestamp').first()
            PrototypeContent.objects.create(content=pttcont.content, prototype=ptt_copy)

        # doc copy
        root_dir = DocumentDir.objects.filter(project=project, par_dir=None).first()
        if root_dir == None:
            return ResponseTemplate(Error.SUCCESS, 'Project is copied successfully!',
                                    data=ProjectSerializer(pro_copy).data)
        root_dir_copy = _init_doc_struction(pro_copy)

        root_docs = Document.objects.filter(par_dir=root_dir, is_deleted=False)
        for root_doc in root_docs:
            root_doc_copy = Document.objects.create(name=root_doc.name, par_dir=root_dir_copy, project=pro_copy)

        sub_dirs = DocumentDir.objects.filter(project=project).exclude(par_dir=None)
        for sub_dir in sub_dirs:
            sub_dir_copy = DocumentDir.objects.create(name=sub_dir.name, par_dir=root_dir_copy, project=pro_copy)
            sub_docs = Document.objects.filter(par_dir=sub_dir, is_deleted=False)
            for sub_doc in sub_docs:
                sub_doc_copy = Document.objects.create(name=sub_doc.name, par_dir=sub_dir_copy, project=pro_copy)

        return ResponseTemplate(Error.SUCCESS, 'Project copy success',
                                data=ProjectSerializer(pro_copy).data)
    except Project.DoesNotExist:
        ResponseTemplate(Error.PRO_NOT_FOUND, 'Project is copied successfully!')
    except Exception as e:
        return ResponseTemplate(Error.FAILED, str(e))