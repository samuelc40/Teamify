from django.contrib import admin
from core.models import *


class TaskAdmin(admin.ModelAdmin):
    list_display = ['title', 'description', 'due_date', 'category']

admin.site.register(Task, TaskAdmin)

admin.site.register(Team)

admin.site.register(Label)

admin.site.register(Comment)