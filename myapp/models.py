from django.db import models
from django.contrib.auth.models import User
from projects.models import Project
from mptt.models import MPTTModel, TreeForeignKey


class Folder(MPTTModel):
    name = models.CharField(max_length=100)
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children', on_delete=models.CASCADE)
    project = TreeForeignKey(Project, related_name='folders', on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    tasks_id = models.ManyToManyField('Task', related_name='folders', blank=True)


class Task(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=200, blank=True, null=True)
    deadline = models.DateTimeField(null=True, blank=True)
    is_completed = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    folder = TreeForeignKey(Folder, related_name='tasks', null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
