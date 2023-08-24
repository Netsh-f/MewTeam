# ------- Litang Save The World! -------
#
# @Time    : 2023/8/24 16:17
# @Author  : Lynx
# @File    : error.py
#

class Error:
    SUCCESS = 0

    # HTTP exception status
    FAILED = -1

    # user modules
    USER_EXISTS = 10001
    EMAIL_EXISTS = 10002
    EMAIL_NOT_FOUND = 10003
    USER_NOT_EXISTS = 10004
    TOKEN_INVALID = 10005

    # message modules

    # team modules
    PERMISSION_DENIED = 30001
    IDENTIFY_ERROR = 30002

    # project modules
    DATABASE_INTERNAL_ERROR = 40001
    DATA_NOT_FOUND = 40002
