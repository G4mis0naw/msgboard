from django.db import models


class messageBoard(models.Model):
    username = models.CharField(max_length=20, null=False, blank=False)
    content = models.TextField(max_length=140, null=False, blank=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']


class usernameInfo(models.Model):
    username = models.CharField(max_length=20, unique=True)
    passwd = models.CharField(max_length=20)
    ticket = models.CharField(max_length=100, default='WTF')
