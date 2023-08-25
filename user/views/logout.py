# ------- Litang Save The World! -------
#
# @Time    : 2023/8/25 9:44
# @Author  : Lynx
# @File    : logout.py
#
from rest_framework.decorators import api_view

from shared.error import Error
from shared.res_temp import ResponseTemplate
from user.models import User


@api_view(['POST'])
def logout(request):
    return ResponseTemplate(Error.SUCCESS, '登出成功！')

@api_view(['POST'])
def logoff(request, user_id):
    user = User.objects.get(id=user_id)
    if user:
        user.delete()
        return ResponseTemplate(Error.SUCCESS, '注销成功！')
    else:
        return ResponseTemplate(Error.USER_NOT_EXISTS, '用户不存在')