from django.contrib import admin
from userauths.models import User

class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'is_staff', 'team_lead']

admin.site.register(User, UserAdmin)
