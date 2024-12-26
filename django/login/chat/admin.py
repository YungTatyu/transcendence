from django.contrib import admin

from .models import Friends

class FriendsAdmin(admin.ModelAdmin):
    list_display = ('pk','user', 'friend',)

admin.site.register(Friends, FriendsAdmin)