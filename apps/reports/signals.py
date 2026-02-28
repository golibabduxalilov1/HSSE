from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import Report, ReportComment, ReportHistory
from apps.notifications.models import Notification
from kafka_app.producer import send_kafka_message
import logging

logger = logging.getLogger(__name__)


@receiver(pre_save, sender=Report)
def track_report_changes(sender, instance, **kwargs):
    
    if instance.pk:
        try:
            old_instance = Report.objects.get(pk=instance.pk)
            
            # Track status change
            if old_instance.status != instance.status:
                ReportHistory.objects.create(
                    report=instance,
                    user=None,  
                    action='Status changed',
                    old_value=old_instance.get_status_display(),
                    new_value=instance.get_status_display()
                )
            
            if old_instance.assignee != instance.assignee:
                ReportHistory.objects.create(
                    report=instance,
                    user=None,
                    action='Assignee changed',
                    old_value=old_instance.assignee.full_name if old_instance.assignee else 'None',
                    new_value=instance.assignee.full_name if instance.assignee else 'None'
                )
        except Report.DoesNotExist:
            pass


@receiver(post_save, sender=Report)
def report_created_notification(sender, instance, created, **kwargs):
    
    if created:
        from apps.accounts.models import User
        admins = User.objects.filter(role__in=['superadmin', 'admin'], is_active=True, is_deleted=False)
        
        for admin in admins:
            Notification.objects.create(
                recipient=admin,
                sender=instance.reporter,
                notification_type='report_created',
                title='Yangi hisobot',
                message=f'{instance.reporter.full_name} yangi hisobot yaratdi: {instance.title}',
                report=instance
            )
        
        try:
            send_kafka_message('report-events', {
                'event': 'report_created',
                'report_id': instance.id,
                'report_code': instance.code,
                'reporter_id': instance.reporter.id,
                'report_type': instance.report_type.type_code,
            })
        except Exception as e:
            logger.error(f"Failed to send Kafka message: {e}")


@receiver(post_save, sender=Report)
def report_assigned_notification(sender, instance, created, **kwargs):
    
    if not created and instance.assignee:
        try:
            old_instance = Report.objects.get(pk=instance.pk)
            if old_instance.assignee != instance.assignee:
                Notification.objects.create(
                    recipient=instance.assignee,
                    sender=None,
                    notification_type='report_assigned',
                    title='Sizga hisobot tayinlandi',
                    message=f'Sizga yangi hisobot tayinlandi: {instance.title}',
                    report=instance
                )
        except Report.DoesNotExist:
            pass


@receiver(post_save, sender=Report)
def report_status_changed_notification(sender, instance, created, **kwargs):
    
    if not created:
        try:
            old_instance = Report.objects.get(pk=instance.pk)
            if old_instance.status != instance.status:
                Notification.objects.create(
                    recipient=instance.reporter,
                    sender=instance.assignee,
                    notification_type='report_status_changed',
                    title='Hisobot holati o\'zgartirildi',
                    message=f'Hisobotingiz holati o\'zgartirildi: {instance.get_status_display()}',
                    report=instance
                )
                
                if instance.status == 'completed' and instance.assignee:
                    Notification.objects.create(
                        recipient=instance.assignee,
                        sender=None,
                        notification_type='report_status_changed',
                        title='Hisobot yakunlandi',
                        message=f'Hisobot yakunlandi: {instance.title}',
                        report=instance
                    )
        except Report.DoesNotExist:
            pass


@receiver(post_save, sender=ReportComment)
def report_comment_notification(sender, instance, created, **kwargs):
    
    if created:
        recipients = []
        
        if instance.report.reporter != instance.user:
            recipients.append(instance.report.reporter)
        
        if instance.report.assignee and instance.report.assignee != instance.user:
            recipients.append(instance.report.assignee)
        
        for recipient in recipients:
            Notification.objects.create(
                recipient=recipient,
                sender=instance.user,
                notification_type='report_comment',
                title='Yangi sharh',
                message=f'{instance.user.full_name} hisobotga sharh qoldirdi',
                report=instance.report
            )