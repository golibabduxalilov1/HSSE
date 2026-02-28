from django.db import models
from django.conf import settings
from core.mixins import TimeStampedMixin, SoftDeleteMixin
from core.utils import get_file_path, generate_unique_code


class Report(TimeStampedMixin, SoftDeleteMixin):

    STATUS_CHOICES = (
        ("new", "Yangi hisobot"),
        ("umumiy", "Umumiy hisobot"),
        ("accepted", "Qabul qilindi"),
        ("in_progress", "Jarayonda"),
        ("on_hold", "Kutilmoqda"),
        ("cancelled", "Bekor qilindi"),
        ("completed", "Yakunlandi"),
    )
    PRIORITY_CHOICES = (
        ("normal", "Normal"),
        ("high", "Yuqori"),
        ("urgent", "Shoshilinch"),
    )

    code = models.CharField(
        max_length=50, unique=True, editable=False, verbose_name="Kod"
    )
    title = models.CharField(max_length=500, verbose_name="Sarlavha")
    description = models.TextField(verbose_name="Tavsif")

    # Turi va toifasi
    report_type = models.ForeignKey(
        "settings.ReportType", on_delete=models.PROTECT, related_name="reports"
    )
    risk_category = models.ForeignKey(
        "settings.RiskCategory",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="reports",
    )

    branch = models.ForeignKey(
        "settings.Branch", on_delete=models.PROTECT, related_name="reports"
    )
    location = models.ForeignKey(
        "settings.Location", on_delete=models.PROTECT, related_name="reports"
    )

    reporter = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="reported_reports",
    )
    assignee = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="assigned_reports",
    )

    # Holat
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="new")
    priority = models.CharField(
        max_length=20, choices=PRIORITY_CHOICES, default="normal"
    )

    start_date = models.DateField(null=True, blank=True)
    deadline = models.DateField(null=True, blank=True)
    completed_date = models.DateField(null=True, blank=True)

    is_anonymous = models.BooleanField(default=False, verbose_name="Anonim")

    class Meta:
        db_table = "reports"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["status", "created_at"]),
            models.Index(fields=["report_type", "status"]),
            models.Index(fields=["assignee", "status"]),
        ]

    def __str__(self):
        return f"{self.code} - {self.title}"

    def save(self, *args, **kwargs):
        if not self.code:
            prefix = self.report_type.type_code.upper()[:3]
            self.code = generate_unique_code(prefix=prefix, length=8)
        super().save(*args, **kwargs)


class ReportAttachment(TimeStampedMixin):

    FILE_TYPE_CHOICES = (
        ("image", "Rasm"),
        ("video", "Video"),
        ("document", "Hujjat"),
    )

    report = models.ForeignKey(
        Report, on_delete=models.CASCADE, related_name="attachments"
    )
    file = models.FileField(upload_to=get_file_path, verbose_name="Fayl")
    file_type = models.CharField(max_length=20, choices=FILE_TYPE_CHOICES)
    file_name = models.CharField(max_length=255)
    file_size = models.IntegerField(verbose_name="Fayl hajmi (bytes)")

    class Meta:
        db_table = "report_attachments"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.report.code} - {self.file_name}"


class ReportComment(TimeStampedMixin, SoftDeleteMixin):

    report = models.ForeignKey(
        Report, on_delete=models.CASCADE, related_name="comments"
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="report_comments",
    )
    comment = models.TextField(verbose_name="Sharh")

    class Meta:
        db_table = "report_comments"
        ordering = ["created_at"]

    def __str__(self):
        return f"{self.report.code} - {self.user.full_name}"


class ReportHistory(TimeStampedMixin):

    report = models.ForeignKey(Report, on_delete=models.CASCADE, related_name="history")
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="report_history",
    )
    action = models.CharField(max_length=100, verbose_name="Harakat")
    old_value = models.TextField(null=True, blank=True)
    new_value = models.TextField(null=True, blank=True)

    class Meta:
        db_table = "report_history"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.report.code} - {self.action}"
