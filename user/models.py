from django.db import models

class User(models.Model):
    email = models.EmailField(max_length=63)
    nickname = models.CharField(max_length=63)
    password = models.CharField(max_length=63)
    phonenum = models.IntegerField()

    class Meta:
        verbose_name = '用户'


