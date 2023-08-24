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
    '''
    请求三个属性：用户昵称，用户邮箱，用户密码
    后端进行的判定有：昵称重复性检测，邮箱重复性检测
    '''
    try:
        data = request.data
        message = ''
        nickname = data['nickname']
        email = data['email']

        if User.objects.filter(nickname=nickname).exists():
            message = '昵称已被注册'
            return Response({'errno': Error.USER_EXISTS, 'msg': message}, status=status.HTTP_200_OK)

        if User.objects.filter(email=email).exists():
            message = '邮箱已被注册'
            return Response({'errno': Error.EMAIL_EXISTS, 'msg': message}, status=status.HTTP_200_OK)

        user = User.objects.create(nickname=nickname, email=email, password=data['password'])
        message = '用户注册成功！'
        return Response({'errno':Error.SUCCESS, 'msg': message}, status=status.HTTP_201_CREATED)
    except KeyError as keyError:
        message = '请求结构体非法'
        return Response({'errno':Error.FAILED, 'msg': message}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as exception:
        message = '服务器异常'
        # print(exception)
        return Response({'errno': Error.FAILED, 'msg': message}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
def login(request):
    '''

    '''
    try:
        data = request.data
        email = data['email']
        message = ''

        if not User.objects.filter(email=email).exists():
            message = '用户不存在'
            return Response({'errno':Error.USER_NOT_EXISTS, 'msg': message}, )
    except KeyError as keyError:
        pass

