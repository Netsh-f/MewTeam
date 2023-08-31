# ------- Litang Save The World! -------
#
# @Time    : 2023/8/25 10:25
# @Author  : Lynx
# @File    : info.py
#

from rest_framework.decorators import api_view

from shared.error import Error
from shared.res_temp import ResponseTemplate
from user.models import User
from user.serializers import UserSerializer


@api_view(['GET'])
def infoShow(request, user_id):
    user = User.objects.filter(id=user_id).first()
    if user != None:
        return ResponseTemplate(Error.SUCCESS, '用户信息返回成功！', data=UserSerializer(user).data)
    else:
        return ResponseTemplate(Error.USER_NOT_EXISTS, '用户不存在')


@api_view(['PUT'])
def infoEdit(request, user_id):
    data: dict = request.data
    try:
        user = User.objects.get(id=user_id)
        name = data.get('name', None)
        nickname = data.get('nickname', None)
        password = data.get('password', None)

        if name is not None:
            user.name = name
        if nickname is not None:
            user.nickname = nickname
        if password is not None:
            user.password = password
        user.save()
        return ResponseTemplate(Error.SUCCESS, '用户信息修改成功！')
    except Exception:
        return ResponseTemplate(Error.USER_NOT_EXISTS, '用户不存在')
