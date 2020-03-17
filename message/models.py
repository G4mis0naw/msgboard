from django.db import models


class messageBoard(models.Model):
    username = models.CharField(max_length=20, null=False, blank=False)
    content = models.TextField(max_length=140, null=False, blank=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']
