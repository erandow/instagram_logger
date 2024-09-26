# Register your models here.

# accounts/admin.py

from django.contrib import admin
from .models import InstagramAccount, Log

class InstagramAccountAdmin(admin.ModelAdmin):
    list_display = ('user', 'username', 'created_at')

class LogAdmin(admin.ModelAdmin):
    list_display = ('account', 'action', 'timestamp')
    list_filter = ('action', 'timestamp')
    search_fields = ['account__username']

admin.site.register(InstagramAccount, InstagramAccountAdmin)
admin.site.register(Log, LogAdmin)

