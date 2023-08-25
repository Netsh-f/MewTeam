from django.utils import timezone

from django.db import models

from user.models import User


class Team(models.Model):
    name = models.CharField(max_length=63)


class UserTeamShip(models.Model):
    class Identify(models.IntegerChoices):
        NORMAL = 0, "Normal"
        ADMIN = 1, "Admin"
        CREATOR = 2, "Creator"

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    team = models.OneToOneField(Team, on_delete=models.CASCADE)
    identify = models.PositiveSmallIntegerField(choices=Identify.choices, default=Identify.NORMAL)


class Invitations(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_invitations')
    receiver_email = models.EmailField()
    invitation_code = models.CharField(max_length=16, unique=True)
    created_at = models.DateTimeField(default=timezone.now)
    used = models.BooleanField(default=False)
