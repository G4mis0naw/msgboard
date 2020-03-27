from django.db import models


class messageBoard(models.Model):
    uUsername = models.ForeignKey('usernameInfo', to_field='username', on_delete=models.DO_NOTHING, default='')
    content = models.TextField(max_length=140, null=False, blank=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']


class usernameInfo(models.Model):
    username = models.CharField(max_length=20, unique=True, verbose_name='username')
    passwd = models.CharField(max_length=20, verbose_name='password')
    tickettoken = models.CharField(max_length=64, null=True, unique=True, verbose_name='status')

    def __str__(self):
        return self.username