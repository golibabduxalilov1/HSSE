from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from .models import Notification


def send_notification(
    recipient, sender, notification_type, title, message, report=None, extra_data=None
):

    notification = Notification.objects.create(
        recipient=recipient,
        sender=sender,
        notification_type=notification_type,
        title=title,
        message=message,
        report=report,
        extra_data=extra_data,
    )

    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f"notifications_{recipient.id}",
        {
            "type": "notification_message",
            "notification": {
                "id": notification.id,
                "type": notification_type,
                "title": title,
                "message": message,
                "created_at": notification.created_at.isoformat(),
            },
        },
    )

    return notification


def send_bulk_notifications(
    recipients, sender, notification_type, title, message, report=None
):

    notifications = []
    for recipient in recipients:
        notification = send_notification(
            recipient=recipient,
            sender=sender,
            notification_type=notification_type,
            title=title,
            message=message,
            report=report,
        )
        notifications.append(notification)

    return notifications
