from django.db import models


class usernameInfo(models.Model):
    username = models.CharField(max_length=20, unique=True)
    passwd = models.CharField(max_length=20)