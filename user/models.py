from django.db import models

class User(models.Model):
    uid = models.BigAutoField(primary_key=True)
    email = models.EmailField(max_length=63)
    username = models.CharField(max_length=63)
    password = models.CharField(max_length=71)
