from django.db import models
from django.utils import timezone

from project.models import Document
from team.models import Team
from user.models import User


class Room(models.Model):
    class RoomType(models.IntegerChoices):
        TEAM = 0, "Team"
        GROUP = 1, "Group"
        PRIVATE = 2, "Private"

    roomName = models.CharField(max_length=63)
    type = models.PositiveSmallIntegerField(choices=RoomType.choices, default=RoomType.TEAM)
    avatar = models.CharField(max_length=127, default='assets/images/people.png')

    team = models.ForeignKey(Team, on_delete=models.CASCADE, null=True)


class UserRoomShip(models.Model):
    class Identify(models.IntegerChoices):
        NORMAL = 0, "Normal"
        ADMIN = 1, "Admin"
        CREATOR = 2, "Creator"

    identify = models.PositiveSmallIntegerField(choices=Identify.choices, default=Identify.NORMAL)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Message(models.Model):
    content = models.TextField(null=True)
    refactor_content = models.TextField(null=True)
    sender_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    timestamp = models.DateTimeField(default=timezone.now)
    room = models.ForeignKey(Room, on_delete=models.CASCADE, null=True)
    mid = models.UUIDField()


class MessageFile(models.Model):
    name = models.CharField(max_length=127)
    size = models.IntegerField()  # Byte
    type = models.CharField(max_length=15)  # example: "image/png"
    extension = models.CharField(max_length=15)  # "png"
    # audio = models.BooleanField(default=False)
    # duration = models.DecimalField(default=0)
    url = models.CharField(max_length=127)
    mid = models.UUIDField()
    message = models.ForeignKey(Message, on_delete=models.CASCADE)


class Mention(models.Model):
    class MentionType(models.IntegerChoices):
        MESSAGE = 0, "Message"
        DOCUMENT = 1, "Document"

    type = models.PositiveSmallIntegerField(choices=MentionType.choices, default=MentionType.MESSAGE)

    @property
    def text(self):
        if self.type == self.MentionType.MESSAGE:
            return self.message.refactor_content if self.message else ""
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
