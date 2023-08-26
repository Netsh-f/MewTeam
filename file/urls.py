# ------- Litang Save The World! -------
#
# @Time    : 2023/8/26 10:33
# @Author  : Lynx
# @File    : urls.py
#
from django.urls import path

from file.views import upload_file

urlpatterns = [
    path("", upload_file),
]