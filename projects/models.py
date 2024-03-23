from django.db import models
from django.contrib.auth.models import User


class Project(models.Model):
    name = models.CharField(max_length=100)
    user = models.ForeignKey(User, blank=True, on_delete=models.CASCADE, null=False)
    members = models.ManyToManyField(User, related_name='projects', blank=True)


class ProjectMember(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
