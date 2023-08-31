from rest_framework.decorators import api_view
from rest_framework import status

from shared.error import Error
from shared.res_temp import ResponseTemplate
from shared import token
from team.models import Team
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
        nickname = data['nickname']
        email = data['email']
        name = data['name']

        if User.objects.filter(nickname=nickname).exists():
            return ResponseTemplate(Error.NICKNAME_EXISTS, '昵称已被注册')
        if User.objects.filter(email=email).exists():
            return ResponseTemplate(Error.EMAIL_EXISTS, '邮箱已被注册')
        if User.objects.filter(email=email).exists():
            return ResponseTemplate(Error.NAME_EXISTS, '真实姓名已被注册')

        user = User.objects.create(nickname=nickname, email=email, name=name, password=data['password'])
        data = {
            'user_id': user.id,
            'token': token.generate_token(user.id)
        }
        return ResponseTemplate(Error.SUCCESS, '用户注册成功！', status=status.HTTP_201_CREATED, data=data)
    except KeyError as keyError:
        return ResponseTemplate(Error.FAILED, '请求结构体非法', status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return ResponseTemplate(Error.FAILED, str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
