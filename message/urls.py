# ------- Litang Save The World! -------
#
# @Time    : 2023/8/24 13:42
# @Author  : Lynx
# @File    : urls.py
#

from django.urls import path
from message.views import history, center, chat

urlpatterns = [
    path('teams/<int:team_id>/messages/history/', history.get_history),
    path('teams/<int:team_id>/messages/', history.retrieve_message_by_date),
    path('mentions/', center.get_mentions),
    path('mentions/<int:mention_id>/read/', center.set_mention_checked),
    path('mentions/messages/read/', center.set_all_message_mention_checked),
    path('mentions/documents/read/', center.set_all_document_mention_checked),
    path('mentions/<int:mention_id>/delete/', center.set_mention_deleted),
    path('mentions/messages/read/delete/', center.set_all_message_read_mention_deleted),
    path('mentions/documents/read/delete/', center.set_all_document_read_mention_deleted),

    path('files/', chat.upload_message_file),
    path('teams/<int:team_id>/rooms/', chat.create_group),
    path('teams/<int:team_id>/rooms/private/', chat.create_private_room),
    path('teams/<int:team_id>/rooms/list/', chat.get_room_list),
    path('rooms/<int:room_id>/history/', chat.get_chat_history),
    path('rooms/<int:room_id>/exit/', chat.exit_room),
    path('rooms/<int:room_id>/dissolve/', chat.dissolve_room),
    path('teams/<int:team_id>/users/list/', chat.get_create_group_user_list),
    path('teams/<int:team_id>/users/list/private/', chat.get_create_private_group_user_list),
    path('rooms/<int:room_id>/messages/search/', chat.search_history_message),
    path('rooms/<int:room_id>/messages/forward/', chat.forward_message),
]
