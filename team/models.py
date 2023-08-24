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
