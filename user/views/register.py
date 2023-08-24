from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from shared.error import Error
from user.models import User

'''
前端更加提倡以不同的HTTP状态码标明错误的种类
Response template:
{
    "errno": 10001,
    "msg": "user already exists",
    "data": {
        "id": 1,
        "nickname": "lynx",
        "email": "111@111.com"
    }
}   
'''

@api_view(['POST'])
def register(request):
    try:
        data = request.data
        nickname = data['nickname']
        email = data['email']

        if User.objects.filter(nickname=nickname).exists():
            message = '用户名已存在'
            return Response({'errno': Error.USER_EXISTS, 'msg': message}, status=status.HTTP_200_OK)

        if User.objects.filter(email=email).exists():
            message = '邮箱已被注册'
            return Response({'errno': Error.EMAIL_NOT_FOUND, 'msg': message}, status=status.HTTP_200_OK)

        user = User.objects.create(nickname=nickname, password=data['password'], email=data['email'])
        message = '用户注册成功！'
        return Response({'errno':Error.SUCCESS, 'msg': message}, status=status.HTTP_201_CREATED)
    except Exception as e:
        message = '请求结构体非法'
        return Response({'errno':Error.FAILED, 'msg': message}, status=status.HTTP_400_BAD_REQUEST)