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

@api_view(['GET'])
def infoShow(request, user_id):
    user = User.objects.get(id=user_id)
    if user:
        return ResponseTemplate(Error.SUCCESS, '用户信息返回成功！', data=user)
    else:
        return ResponseTemplate(Error.USER_NOT_EXISTS, '用户不存在')

@api_view(['POST'])
def infoEdit(request, user_id):
    data = request.data
    # user = User.objects.get(id=user_id)
    # if user:
    #     if data.get('name'):
    # #     return ResponseTemplate(Error.SUCCESS, '用户信息返回成功！', data=user)
    # else:
    #     return ResponseTemplate(Error.USER_NOT_EXISTS, '用户不存在')