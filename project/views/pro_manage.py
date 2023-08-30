# ------- Litang Save The World! -------
#
# @Time    : 2023/8/25 16:29
# @Author  : Lynx
# @File    : pro_manage.py
#
from datetime import timedelta, datetime

from django.db.models import Q
from rest_framework.decorators import api_view

from project.models import Project
from project.serializers import ProjectSerializer
from project.views.utils.safety_check import _is_legal_identity
from shared.error import Error
from shared.res_temp import ResponseTemplate
from shared.token import check_token


# Create your views here.

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
def update_project(request, team_id, pro_id):
    try:
        response, user_id = check_token(request)
        if user_id == -1:
            return response
        data = request.data
        name = data['name']
        if not _is_legal_identity(user_id, team_id):
            return ResponseTemplate(Error.ILLEGAL_IDENTITY, '非法更改，请检查您的用户状态和团队信息')

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
def delete_project(request, team_id, pro_id):
    try:
        response, user_id = check_token(request)
        if user_id == -1:
            return response
        if not _is_legal_identity(user_id, team_id):
            return ResponseTemplate(Error.ILLEGAL_IDENTITY, '非法删除，请检查您的用户状态和团队信息')

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
def recover_project(request, team_id, pro_id):
    try:
        response, user_id = check_token(request)
        if user_id == -1:
            return response
        if not _is_legal_identity(user_id, team_id):
            return ResponseTemplate(Error.ILLEGAL_IDENTITY, '非法恢复，请检查您的用户状态和团队信息')

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
def destroy_project(request, team_id, pro_id):
    try:
        response, user_id = check_token(request)
        if user_id == -1:
            return response
        if not _is_legal_identity(user_id, team_id):
            return ResponseTemplate(Error.ILLEGAL_IDENTITY, '非法清空，请检查您的用户状态和团队信息')

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

def search_project(request, team_id):
    try:
        response, user_id = check_token(request)
        if user_id == -1:
            return response
        if not _is_legal_identity(user_id, team_id):
            return ResponseTemplate(Error.ILLEGAL_IDENTITY, '非法搜索，请检查您的用户状态和团队信息')

        name = request.data

    except KeyError as keyError:
        return ResponseTemplate(Error.FAILED, 'Invalid or missing key')

    except Exception as e:
        return ResponseTemplate(Error.FAILED, str(e))