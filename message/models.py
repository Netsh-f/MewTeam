from django.db import models
from django.utils import timezone

from team.models import Team
from user.models import User


class Message(models.Model):
    class MessageType(models.IntegerChoices):
        TEXT = 0, "Text"
        IMAGE = 1, "Image"
        FILE = 2, "FILE"

    sender_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    receiver_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')  # 群聊时为空
    team = models.ForeignKey(Team, on_delete=models.CASCADE)  # 私聊时为空
    timestamp = models.DateTimeField(default=timezone.now())
    mtype = models.PositiveSmallIntegerField(choices=MessageType.choices, default=MessageType.TEXT)
    checked = models.BooleanField(default=False)
    text = models.TextField()
    file_path = models.CharField(max_length=127)
