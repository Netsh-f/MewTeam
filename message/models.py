from django.db import models
from django.utils import timezone

from project.models import Document
from team.models import Team
from user.models import User


class Session(models.Model):
    users = models.ManyToManyField(User, related_name='sessions')
    session_id = models.CharField(max_length=15, unique=True)


class Message(models.Model):
    class MessageType(models.IntegerChoices):
        TEXT = 0, "Text"
        IMAGE = 1, "Image"
        FILE = 2, "FILE"

    class RoomType(models.IntegerChoices):
        GROUP = 0, "Group"
        PRIVATE = 1, "Private"

    sender_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    receiver_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages',
                                      null=True)  # 群聊时为空
    sender_deleted = models.BooleanField(default=False)
    receiver_deleted = models.BooleanField(default=False)
    session = models.ForeignKey(Session, on_delete=models.CASCADE, null=True)
    room_type = models.PositiveSmallIntegerField(choices=RoomType.choices, default=RoomType.GROUP)
    team = models.ForeignKey(Team, on_delete=models.CASCADE, null=True)  # 私聊时为空
    timestamp = models.DateTimeField(default=timezone.now)
    mtype = models.PositiveSmallIntegerField(choices=MessageType.choices, default=MessageType.TEXT)
    checked = models.BooleanField(default=False)
    text = models.TextField(null=True)
    file = models.CharField(max_length=127, null=True)


class Mention(models.Model):
    class MentionType(models.IntegerChoices):
        MESSAGE = 0, "Message"
        DOCUMENT = 1, "Document"

    type = models.PositiveSmallIntegerField(choices=MentionType.choices, default=MentionType.MESSAGE)

    @property
    def text(self):
        if self.type == self.MentionType.MESSAGE:
            return self.message.text if self.message else ""
        elif self.type == self.MentionType.DOCUMENT:
            return self.document.name if self.document else ""
        return ""

    sender_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_mention')
    receiver_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_mention')
    sender_deleted = models.BooleanField(default=False)
    receiver_deleted = models.BooleanField(default=False)
    message = models.ForeignKey(Message, on_delete=models.CASCADE, null=True)
    document = models.ForeignKey(Document, on_delete=models.CASCADE, null=True)
    timestamp = models.DateTimeField(default=timezone.now)
    checked = models.BooleanField(default=False)

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=models.Q(message__isnull=False) | models.Q(document__isnull=False),
                name='message_xor_document'
            )
        ]
