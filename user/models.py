from django.db import models

from MewTeam import settings


class User(models.Model):
    email = models.EmailField(max_length=63)
    nickname = models.CharField(max_length=63)
    password = models.CharField(max_length=63)
    name = models.CharField(max_length=63)
    avatar = models.CharField(max_length=127, default=f"{settings.AVATAR_URL}default.jpg")

    class Meta:
        verbose_name = '用户'
