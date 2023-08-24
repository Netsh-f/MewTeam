# ------- Litang Save The World! -------
#
# @Time    : 2023/8/24 13:43
# @Author  : Lynx
# @File    : urls.py
#
from django.urls import path

from user.views import register

urlpatterns = [
    path('register', register.register, name='register'),

]