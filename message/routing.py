# ------- Litang Save The World! -------
#
# @Time    : 2023/9/2 19:45
# @Author  : Lynx
# @File    : routing.py
#
from django.urls import re_path

from message.consumers import ChatConsumer

websocket_urlpatterns = [
    re_path(r"ws/message/(?P<team_id>\w+)/$", ChatConsumer.as_asgi()),
    # re_path(r"ws/prototype/(?P<ptt_id>\w+)/$", PttConsumer.as_asgi()),
]