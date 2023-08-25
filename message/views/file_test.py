# ------- Litang Save The World! -------
#
# @Time    : 2023/8/26 0:38
# @Author  : Lynx
# @File    : file_test.py
#
from rest_framework.decorators import api_view

from MewTeam.settings import MEDIA_ROOT
from message.models import Message
from shared.error import Error
from shared.res_temp import ResponseTemplate


@api_view(['POST'])
def img_receive(request):
    file = request.FILES['file']
    filepath = MEDIA_ROOT + file.name
    Message.objects.update(filepath=filepath)

    with open(filepath, 'wb') as dest_file:
        for chunk in file.chunks():
            dest_file.write(chunk)

    return ResponseTemplate(Error.SUCCESS, '接收成功')