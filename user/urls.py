# ------- Litang Save The World! -------
#
# @Time    : 2023/8/24 13:43
# @Author  : Lynx
# @File    : urls.py
#
from django.urls import path

from user.views import register, login, logout, info, profile

urlpatterns = [
    path('register/', register.register, name='register'),
    path('login/', login.login, name='login'),
    path('logout/', logout.logout, name='logout'),
    path('logoff/<int:user_id>/', logout.logoff),
    path('info/show/<int:user_id>/', info.infoShow, name='infoShow'),
    path('info/edit/<int:user_id>/', info.infoEdit, name='infoEdit'),
    path('profile/avatar/', profile.edit_user_avatar),
    path('<int:user_id>/view/avatar/', profile.view_user_avatar),
]
