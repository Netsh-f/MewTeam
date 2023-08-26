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

    # global error
    DATABASE_INTERNAL_ERROR = 1001
    DATA_NOT_FOUND = 1002

    # user modules
    NICKNAME_EXISTS = 10001
    EMAIL_EXISTS = 10002
    NAME_EXISTS = 10003
    EMAIL_NOT_FOUND = 10004
    USER_NOT_EXISTS = 10005
    TOKEN_INVALID = 10006
    PASSWORD_NOT_CORRECT = 10007

    # message modules
    INVALID_DATE_FORMAT = 20001

    # team modules
    PERMISSION_DENIED = 30001
    IDENTIFY_ERROR = 30002
    TEAM_NOT_EXISTS = 30003
    INVALID_INVITATION_CODE = 30004

    # project modules
    ILLEGAL_IDENTITY = 40001
    PRO_NAME_EXISTS = 40002
    PRO_NOT_FOUND = 40003
    # 这里的身份错误有三种：用户不存在，团队不存在，用户不在团队中

    # file
    FILE_MISSING = 50001
    FILE_TYPE_INVALID = 50002
    FILE_SIZE_ILLEGAL = 50003
