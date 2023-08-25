# ------- Litang Save The World! -------
#
# @Time    : 2023/8/24 13:42
# @Author  : Lynx
# @File    : urls.py
#

from django.urls import path
from message import views
from message.views.history import get_history

urlpatterns = [
    path('teams/<int:team_id>/message/history/', get_history)
]

