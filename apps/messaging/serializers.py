from rest_framework import serializers
from .models import Conversation, Message, MessageReadReceipt
from apps.accounts.serializers import UserSerializer


class MessageSerializer(serializers.ModelSerializer):

    sender = UserSerializer(read_only=True)

    class Meta:
        model = Message
        fields = [
            "id",
            "conversation",
            "sender",
            "message_type",
            "content",
            "file",
            "is_read",
            "read_at",
            "created_at",
        ]
        read_only_fields = ["id", "sender", "is_read", "read_at", "created_at"]


class ConversationSerializer(serializers.ModelSerializer):

    participants = UserSerializer(many=True, read_only=True)
    unread_count = serializers.SerializerMethodField()

    class Meta:
        model = Conversation
        fields = [
            "id",
            "participants",
            "last_message",
            "last_message_at",
            "unread_count",
            "created_at",
        ]
        read_only_fields = ["id", "last_message", "last_message_at", "created_at"]

    def get_unread_count(self, obj):
        user = self.context.get("request").user
        return obj.messages.filter(is_read=False).exclude(sender=user).count()


class ConversationDetailSerializer(serializers.ModelSerializer):

    participants = UserSerializer(many=True, read_only=True)
    messages = MessageSerializer(many=True, read_only=True)

    class Meta:
        model = Conversation
        fields = [
            "id",
            "participants",
            "messages",
            "last_message",
            "last_message_at",
            "created_at",
        ]
