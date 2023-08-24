# ------- Litang Save The World! -------
#
# @Time    : 2023/8/24 17:41
# @Author  : Lynx
# @File    : res_temp.py
#

class ResponseTemplate:
    def resTemp(self, errno: int, msg: str, data: dict = None) -> json:
        if data:
            return {'errno': errno, 'msg': msg, 'data': data}
        else:
            return {'errno': errno, 'msg': msg}