# ------- Litang Save The World! -------
#
# @Time    : 2023/8/24 13:43
# @Author  : Lynx
# @File    : urls.py
#
from django.urls import path

from user.views import register, login, logout

urlpatterns = [
    path('register', register.register, name='register'),
    path('login', login.login, name='login'),
    path('logout', logout.logout, name='logout'),
    path('writeoff/<int:user_id>', logout.writeoff, name='writeoff')
]