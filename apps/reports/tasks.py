from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from .models import Report
from apps.notifications.utils import send_notification
import logging

logger = logging.getLogger(__name__)


@shared_task
def send_report_deadline_reminder():

    from django.utils import timezone
    from datetime import timedelta

    tomorrow = timezone.now().date() + timedelta(days=1)
    day_after = timezone.now().date() + timedelta(days=2)

    reports = Report.objects.filter(
        deadline__gte=tomorrow,
        deadline__lte=day_after,
        status__in=["new", "in_progress"],
        is_deleted=False,
    ).select_related("assignee", "reporter")

    for report in reports:
        if report.assignee:
            send_notification(
                recipient=report.assignee,
                sender=None,
                notification_type="system",
                title="Hisobot muddati tugamoqda",
                message=f'Hisobot "{report.title}" muddati {report.deadline} gacha',
                report=report,
            )

    logger.info(f"Sent deadline reminders for {reports.count()} reports")
    return f"Processed {reports.count()} reports"


@shared_task
def generate_daily_report_summary():

    from django.utils import timezone
    from datetime import timedelta
    from django.db.models import Count

    today = timezone.now().date()
    yesterday = today - timedelta(days=1)

    reports = Report.objects.filter(created_at__date=yesterday, is_deleted=False)

    summary = {
        "date": str(yesterday),
        "total_reports": reports.count(),
        "by_type": dict(
            reports.values("report_type__type_code")
            .annotate(count=Count("id"))
            .values_list("report_type__type_code", "count")
        ),
        "by_status": dict(
            reports.values("status")
            .annotate(count=Count("id"))
            .values_list("status", "count")
        ),
    }

    logger.info(f"Daily summary: {summary}")
    return summary


@shared_task
def cleanup_old_notifications():

    from django.utils import timezone
    from datetime import timedelta
    from apps.notifications.models import Notification

    threshold_date = timezone.now() - timedelta(days=30)

    deleted_count = Notification.objects.filter(
        created_at__lt=threshold_date, is_read=True
    ).delete()[0]

    logger.info(f"Deleted {deleted_count} old notifications")
    return f"Deleted {deleted_count} notifications"
