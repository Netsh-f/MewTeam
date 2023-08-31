# ------- Litang Save The World! -------
#
# @Time    : 2023/8/31 10:01
# @Author  : Lynx
# @File    : routing.py
#
from django.urls import re_path

from project import consumers

websocket_urlpatterns = [
    re_path(r"ws/prototype/(?P<room_id>\w+)/$", consumers.ChatConsumer.as_asgi()),
]