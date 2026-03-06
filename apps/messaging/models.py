from django.db import models
from django.conf import settings
from core.mixins import TimeStampedMixin, SoftDeleteMixin
from core.utils import get_file_path


class Conversation(TimeStampedMixin, SoftDeleteMixin):

    participants = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="conversations",
        verbose_name="Ishtirokchilar",
    )
    last_message = models.TextField(null=True, blank=True, verbose_name="Oxirgi xabar")
    last_message_at = models.DateTimeField(
        null=True, blank=True, verbose_name="Oxirgi xabar vaqti"
    )

    class Meta:
        db_table = "conversations"
        verbose_name = "Suhbat"
        verbose_name_plural = "Suhbatlar"
        ordering = ["-last_message_at"]

    def __str__(self):
        return f"Conversation {self.id}"


class Message(TimeStampedMixin, SoftDeleteMixin):

    MESSAGE_TYPE_CHOICES = (
        ("text", "Matn"),
        ("image", "Rasm"),
        ("video", "Video"),
        ("audio", "Audio"),
        ("file", "Fayl"),
    )

    conversation = models.ForeignKey(
        Conversation,
        on_delete=models.CASCADE,
        related_name="messages",
        verbose_name="Suhbat",
    )
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="sent_messages",
        verbose_name="Yuboruvchi",
    )
    message_type = models.CharField(
        max_length=20,
        choices=MESSAGE_TYPE_CHOICES,
        default="text",
        verbose_name="Xabar turi",
    )
    content = models.TextField(null=True, blank=True, verbose_name="Matn")
    file = models.FileField(
        upload_to=get_file_path, null=True, blank=True, verbose_name="Fayl"
    )
    is_read = models.BooleanField(default=False, verbose_name="O'qilgan")
    read_at = models.DateTimeField(null=True, blank=True, verbose_name="O'qilgan vaqt")

    class Meta:
        db_table = "messages"
        verbose_name = "Xabar"
        verbose_name_plural = "Xabarlar"
        ordering = ["created_at"]
        indexes = [
            models.Index(fields=["conversation", "created_at"]),
            models.Index(fields=["sender", "is_read"]),
        ]

    def __str__(self):
        return f"{self.sender.full_name} - {self.created_at}"


class MessageReadReceipt(TimeStampedMixin):

    message = models.ForeignKey(
        Message,
        on_delete=models.CASCADE,
        related_name="read_receipts",
        verbose_name="Xabar",
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="message_receipts",
        verbose_name="Foydalanuvchi",
    )
    read_at = models.DateTimeField(auto_now_add=True, verbose_name="O'qilgan vaqt")

    class Meta:
        db_table = "message_read_receipts"
        verbose_name = "Xabar o'qilganlik belgisi"
        verbose_name_plural = "Xabar o'qilganlik belgilari"
        unique_together = ["message", "user"]
        ordering = ["-read_at"]

    def __str__(self):
        return f"{self.message.id} - {self.user.full_name}"
