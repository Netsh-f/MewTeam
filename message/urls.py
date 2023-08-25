# ------- Litang Save The World! -------
#
# @Time    : 2023/8/24 13:42
# @Author  : Lynx
# @File    : urls.py
#

from django.urls import path
from message import views

urlpatterns = [
    path('teams/<int:team_id>/message/history/')
]

