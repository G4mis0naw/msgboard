from django.contrib import admin
from message import models


admin.site.register(models.messageBoard)
admin.site.register(models.usernameInfo)