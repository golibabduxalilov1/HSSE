import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

app = Celery("tmk_hsse")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()


# Periodic tasks
app.conf.beat_schedule = {
    "send-deadline-reminders": {
        "task": "apps.reports.tasks.send_report_deadline_reminder",
        "schedule": crontab(hour=9, minute=0),  # Every day at 9:00 AM
    },
    "generate-daily-summary": {
        "task": "apps.reports.tasks.generate_daily_report_summary",
        "schedule": crontab(hour=23, minute=0),  # Every day at 11:00 PM
    },
    "cleanup-old-notifications": {
        "task": "apps.reports.tasks.cleanup_old_notifications",
        "schedule": crontab(hour=2, minute=0, day_of_week=0),  # Every Sunday at 2:00 AM
    },
}


@app.task(bind=True)
def debug_task(self):
    print(f"Request: {self.request!r}")
