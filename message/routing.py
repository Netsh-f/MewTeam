from django.urls import re_path

from message import consumers

websocket_urlpatterns = [
    re_path(r"ws/message/(?P<room_id>\w+)/$", consumers.ChatConsumer.as_asgi()),
]