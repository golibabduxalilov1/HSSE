from rest_framework import serializers
from .models import Notification
from apps.accounts.serializers import UserSerializer
from apps.reports.serializers import ReportListSerializer


class NotificationSerializer(serializers.ModelSerializer):

    sender = UserSerializer(read_only=True)
    report = ReportListSerializer(read_only=True)
    notification_type_display = serializers.CharField(
        source="get_notification_type_display", read_only=True
    )

    class Meta:
        model = Notification
        fields = [
            "id",
            "recipient",
            "sender",
            "notification_type",
            "notification_type_display",
            "title",
            "message",
            "report",
            "is_read",
            "read_at",
            "extra_data",
            "created_at",
        ]
        read_only_fields = ["id", "recipient", "sender", "created_at"]


class NotificationListSerializer(serializers.ModelSerializer):

    sender_name = serializers.CharField(source="sender.full_name", read_only=True)

    class Meta:
        model = Notification
        fields = [
            "id",
            "sender_name",
            "notification_type",
            "title",
            "message",
            "is_read",
            "created_at",
        ]
