from django.contrib import admin
from . models import ActivityFeed, Task


admin.site.register(Task)
admin.site.register(ActivityFeed)
# Register your models here.
