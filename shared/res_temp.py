# ------- Litang Save The World! -------
#
# @Time    : 2023/8/24 17:41
# @Author  : Lynx
# @File    : res_temp.py
#
from rest_framework import status
from rest_framework.response import Response


class ResponseDictTemplate(dict):
    def __init__(self, errno: int, msg: str, data: dict = None):
        response_data = {'errno': errno, 'msg': msg}
        if data:
            response_data['data'] = data
        super().__init__(response_data)


class ResponseTemplate(Response):
    def __init__(self, errno: int, msg: str, data: dict = None, http_status: int = status.HTTP_200_OK):
        super().__init__(ResponseDictTemplate(errno, msg, data), status=http_status)
