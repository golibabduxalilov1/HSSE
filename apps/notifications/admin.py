from django.contrib import admin

from .models import *


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):

    list_display = ("recipient", "notification_type", "title", "is_read", "created_at")
