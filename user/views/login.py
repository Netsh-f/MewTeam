# ------- Litang Save The World! -------
#
# @Time    : 2023/8/25 9:42
# @Author  : Lynx
# @File    : login.py
#
from rest_framework import status
from rest_framework.decorators import api_view

from shared import token
from shared.error import Error
from shared.res_temp import ResponseTemplate
from user.models import User


@api_view(['POST'])
def login(request):
    '''
    请求参数：email, password
    响应参数: token
    '''
    try:
        data = request.data
        email = data['email']
        password = data['password']

        if not User.objects.filter(email=email):
            return ResponseTemplate(Error.EMAIL_NOT_FOUND, '用户不存在')

        user = User.objects.get(email=email)
        if user.password != password:
            return ResponseTemplate(Error.PASSWORD_NOT_CORRECT, '密码错误')

        return ResponseTemplate(Error.SUCCESS, '登陆成功！', {'token': token.generate_token(user.id)} )
    except KeyError as keyError:
        return ResponseTemplate(Error.FAILED, '请求结构体非法', status=status.HTTP_400_BAD_REQUEST)
    except Exception as exception:
        return ResponseTemplate(Error.FAILED, '服务器异常', status=status.HTTP_500_INTERNAL_SERVER_ERROR)