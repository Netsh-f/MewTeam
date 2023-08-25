# ------- Litang Save The World! -------
#
# @Time    : 2023/8/25 16:29
# @Author  : Lynx
# @File    : curd.py
#
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
    print("___________________step here_______________________")
    response, user_id = check_token(request)
    if user_id == -1:
        return response
    data = request.data
    name = data['name']
    if not _is_legal_identity(user_id, team_id):
        return ResponseTemplate(Error.ILLEGAL_IDENTITY, '非法创建，请检查您的用户状态和团队信息')
    project = Project.objects.create(name=name, team_id=team_id)
    project.save()
    return ResponseTemplate(Error.SUCCESS, '创建成功！', data=ProjectSerializer(project))

@api_view(['PUT'])
def update_project(request, team_id):
    response, user_id = check_token(request)
    if user_id == -1:
        return response
    data = request.data
    name = data['name']
    if not _is_legal_identity(user_id, team_id):
        return ResponseTemplate(Error.ILLEGAL_IDENTITY, '非法更改，请检查您的用户状态和团队信息')
    Project.objects.filter(team_id=team_id).update(name=name)
    return ResponseTemplate(Error.SUCCESS, '修改成功！')

@api_view(['DELETE'])
def delete_project(request, team_id):
    response, user_id = check_token(request)
    if user_id == -1:
        return response
    data = request.data
    name = data['name']
    if not _is_legal_identity(user_id, team_id):
        return ResponseTemplate(Error.ILLEGAL_IDENTITY, '非法删除，请检查您的用户状态和团队信息')
    Project.objects.filter().update(name=name)
    return ResponseTemplate(Error.SUCCESS, '修改成功！')