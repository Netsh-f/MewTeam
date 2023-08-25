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
    receiver_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages',
                                      null=True)  # 群聊时为空
    team = models.ForeignKey(Team, on_delete=models.CASCADE, null=True)  # 私聊时为空
    timestamp = models.DateTimeField(default=timezone.now)
    mtype = models.PositiveSmallIntegerField(choices=MessageType.choices, default=MessageType.TEXT)
    checked = models.BooleanField(default=False)
    text = models.TextField()
    file_path = models.FileField(upload_to='res/msg/')
    text = models.TextField(null=True)
    file_path = models.FileField(upload_to='res/msg/', null=True)

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=models.Q(receiver_user__isnull=False) | models.Q(team__isnull=False),
                name='receiver_user_xor_team'
            )
        ]
