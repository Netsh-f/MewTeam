# from django.urls import re_path
#
# from message.consumers import ChatConsumer
# from project.consumers import PttConsumer
#
# websocket_urlpatterns = [
#     re_path(r"ws/message/(?P<team_id>\w+)/$", ChatConsumer.as_asgi()),
#     re_path(r"ws/prototype/(?P<ptt_id>\w+)/$", PttConsumer.as_asgi()),
# ]