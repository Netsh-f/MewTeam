import json
import logging
from urllib.parse import parse_qs

from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync

from message.models import Message, Mention
from message.serializers import MessageSerializer
from shared.token import verify_token, get_identity_from_token

logger = logging.getLogger(__name__)


class ChatConsumer(WebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user_id = None
        self.room_group_name = None
        self.room_id = None

    def connect(self):
        try:
            query_string = self.scope['query_string'].decode('utf-8')
            query_params = parse_qs(query_string)
            token = query_params.get('token', [''])[0]
            if not verify_token(token):
                self.close()
                return

            self.user_id = get_identity_from_token(token)
            self.room_id = self.scope["url_route"]["kwargs"]["team_id"]
            self.room_group_name = f"chat_{self.room_id}"

            async_to_sync(self.channel_layer.group_add)(
                self.room_group_name, self.channel_name
            )
            self.accept()
        except Exception as e:
            logger.error(str(e))
            self.close()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )

    def receive(self, text_data=None, bytes_data=None):
        try:
            logger.error("---???text_data=" + text_data)
            text_data = json.loads(text_data)

            content = text_data.get("content", None)
            room_id = text_data.get("roomId", None)
            message = Message.objects.create(content=content, sender_user_id=self.user_id, room_id=room_id)
            mention_user_id_list = text_data.get('mention_user_id_list', None)

            if mention_user_id_list is not None:
                for user_id in mention_user_id_list:
                    Mention.objects.create(sender_user_id=self.user_id, receiver_user_id=user_id, message=message)
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name, {"type": "chat.message", "data": MessageSerializer(message).data}
            )
        except Exception as e:
            logger.error(str(e))

    def chat_message(self, event):
        # message = event["message"]
        logger.error('in chat_message, event: ' + str(event))

        # Send message to WebSocket
        self.send(text_data=json.dumps({"message": event}))
