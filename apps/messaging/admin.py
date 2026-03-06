from django.contrib import admin

from unfold.admin import ModelAdmin

from .models import Conversation, Message, MessageReadReceipt


@admin.register(Conversation)
class ConversationAdmin(ModelAdmin):
    list_display = ("id", "last_message", "last_message_at", "created_at")
    filter_horizontal = ("participants",)
    search_fields = ("participants__full_name", "participants__email")


@admin.register(Message)
class MessageAdmin(ModelAdmin):
    list_display = (
        "id",
        "conversation",
        "sender",
        "message_type",
        "is_read",
        "created_at",
    )
    list_filter = ("message_type", "is_read", "created_at")
    search_fields = ("content", "sender__full_name")


@admin.register(MessageReadReceipt)
class MessageReadReceiptAdmin(ModelAdmin):
    list_display = ("id", "message", "user", "read_at")
    list_filter = ("read_at",)
    search_fields = ("user__full_name", "message__id")
