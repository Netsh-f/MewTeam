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
    NICKNAME_EXISTS = 10001
    EMAIL_EXISTS = 10002
    NAME_EXISTS = 10003
    EMAIL_NOT_FOUND = 10004
    USER_NOT_EXISTS = 10005
    TOKEN_INVALID = 10006
    PASSWORD_NOT_CORRECT = 10007

    # message modules

    # team modules
    PERMISSION_DENIED = 30001
    IDENTIFY_ERROR = 30002
    TEAM_NOT_EXISTS = 30003

    # project modules
    DATABASE_INTERNAL_ERROR = 40001
    DATA_NOT_FOUND = 40002

