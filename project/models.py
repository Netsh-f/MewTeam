from django.db import models
from django.utils import timezone

from team.models import Team


# Create your models here.

class Project(models.Model):
    name = models.CharField(max_length=63)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    is_deleted = models.BooleanField(default=False)
    delete_time = models.DateTimeField(null=True)


class Document(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    content = models.JSONField()
    timestamp = models.DateTimeField(default=timezone.now)


class Prototype(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    content = models.JSONField()
    timestamp = models.DateTimeField(default=timezone.now)
