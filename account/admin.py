from django.contrib import admin
from . import models

admin.site.register(models.User)
admin.site.register(models.Committee)
admin.site.register(models.Role)
admin.site.register(models.Member)
