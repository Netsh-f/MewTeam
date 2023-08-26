# ------- Litang Save The World! -------
#
# @Time    : 2023/8/26 10:02
# @Author  : Lynx
# @File    : files.py
#
from django.core.files.uploadedfile import UploadedFile


class MewFileManager(UploadedFile):
    def __init__(self, file: UploadedFile):
        super().__init__(file)

    # def __
