from django.contrib import admin
from unfold.admin import ModelAdmin

from .models import *


@admin.register(Notification)
class NotificationAdmin(ModelAdmin):
    list_display = (
        "id",
        "recipient",
        "sender",
        "notification_type",
        "title",
        "is_read",
        "created_at",
    )
    list_filter = ("notification_type", "is_read", "created_at")
    search_fields = ("recipient__full_name", "recipient__email", "title", "message")
