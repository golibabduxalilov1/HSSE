from django.db import models
from django.conf import settings
from core.mixins import TimeStampedMixin

<<<<<<< HEAD
=======

class Notification(TimeStampedMixin):
    TYPE_CHOICES = (
        ('report_created', 'Yangi hisobot'),
        ('report_assigned', 'Hisobot tayinlandi'),
        ('report_status_changed', 'Hisobot holati o\'zgartirildi'),
        ('report_comment', 'Yangi sharh'),
        ('message_received', 'Yangi xabar'),
        ('system', 'Tizim xabari'),
    )
    
    recipient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='notifications',
        verbose_name='Qabul qiluvchi'
    )
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='sent_notifications',
        verbose_name='Yuboruvchi'
    )
    notification_type = models.CharField(
        max_length=50,
        choices=TYPE_CHOICES,
        verbose_name='Bildirishnoma turi'
    )
    title = models.CharField(max_length=255, verbose_name='Sarlavha')
    message = models.TextField(verbose_name='Xabar')
    
    report = models.ForeignKey(
        'reports.Report',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='notifications',
        verbose_name='Hisobot'
    )
    
    is_read = models.BooleanField(default=False, verbose_name='O\'qilgan')
    read_at = models.DateTimeField(null=True, blank=True, verbose_name='O\'qilgan vaqt')
    
    extra_data = models.JSONField(null=True, blank=True, verbose_name='Qo\'shimcha ma\'lumot')
    
    class Meta:
        db_table = 'notifications'
        verbose_name = 'Bildirishnoma'
        verbose_name_plural = 'Bildirishnomalar'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['recipient', 'is_read', 'created_at']),
            models.Index(fields=['notification_type', 'created_at']),
        ]

    def __str__(self):
        return f"{self.recipient.full_name} - {self.title}"
>>>>>>> fbf1b5d (Complete BranchDetailView and Change Accounts)
