# ------- Litang Save The World! -------
#
# @Time    : 2023/8/31 10:01
# @Author  : Lynx
# @File    : consumers.py
#
import json
import logging
from urllib.parse import parse_qs

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from channels.layers import get_channel_layer

from shared.token import verify_token, get_identity_from_token

logger = logging.getLogger(__name__)

async def get_channel_group_size(group_name):
    channel_layer = get_channel_layer()
    group_channels = await channel_layer.group_channels(group_name)
    return len(group_channels)

class PttConsumer(WebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user_id = None
        self.room_id = None
        # same as ptt_id
        self.room_name = None

    def connect(self):
        try:
            query_string = self.scope['query_string'].decode('utf-8')
            query_params = parse_qs(query_string)
            token = query_params.get('token', [''])[0]
            if not verify_token(token):
                self.close()
                return

            self.user_id = get_identity_from_token(token)
            self.room_id = self.scope["url_route"]["kwargs"]["ptt_id"]
            self.room_name = f"ptt_{self.room_id}"

            async_to_sync(self.channel_layer.group_add)(
                self.room_name, self.channel_name
            )
            self.accept()
        except Exception as e:
            logger.error(str(e))
            self.close()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_name, self.channel_name
        )

    def receive(self, text_data=None, bytes_data=None):
        # 前端调用，receive接受
        try:
            text_data_json = json.loads(text_data)
            logger.info(text_data_json)

            # content = text_data_json.get("content", None)
            # message = Message.objects.create(content=content, sender_user_id=self.user_id, room_id=self.room_id)
            # mention_user_id_list = text_data_json.get('mention_user_id_list', None)
            #
            # if mention_user_id_list is not None:
            #     for user_id in mention_user_id_list:
            #         Mention.objects.create(sender_user_id=self.user_id, receiver_user_id=user_id, message=message)
            # async_to_sync(self.channel_layer.group_send)(
            #     self.room_name, {"type": "chat.message", "data": MessageSerializer(message).data}
            # )
            # user_num = get_channel_group_size(self.room_name)
            data = {
                'id': self.user_id,
                'cursor_x': text_data_json.get('cursor_x', None),
                'cursor_y': text_data_json.get('cursor_y', None)
            }
            async_to_sync(self.channel_layer.group_send)(
                self.room_name, {
                    "type": "chat.message",
                    "data": data
                }
            )
        except Exception as e:
            logger.error(str(e))

    def chat_message(self, event):
        # 发送给前端
        data = event["data"]
        self.send(text_data=json.dumps({"data": data}))
