# ------- Litang Save The World! -------
#
# @Time    : 2023/8/24 13:42
# @Author  : Lynx
# @File    : urls.py
#

from django.urls import path
from message.views import history, center

urlpatterns = [
    path('teams/<int:team_id>/messages/history/', history.get_history),
    path('teams/<int:team_id>/messages/', history.retrieve_message_by_date),
    path('mentions/', center.get_mentions),
    path('mentions/<int:mention_id>/read/', center.set_mention_checked),
    path('mentions/all/read/', center.set_all_mention_checked),
    path('mentions/<int:mention_id>/delete/', center.set_mention_deleted),
    path('mentions/read/delete/', center.set_all_read_mention_deleted),
]
