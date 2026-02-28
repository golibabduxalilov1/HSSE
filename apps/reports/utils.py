from django.db.models import Count, Q
from .models import Report


def get_report_statistics(user, filters=None):
    """Get report statistics for user"""
    
    if user.is_admin():
        queryset = Report.objects.filter(is_deleted=False)
    else:
        queryset = Report.objects.filter(
            Q(reporter=user) | Q(assignee=user),
            is_deleted=False
        )
    
    if filters:
        if 'branch' in filters:
            queryset = queryset.filter(branch_id=filters['branch'])
        if 'report_type' in filters:
            queryset = queryset.filter(report_type_id=filters['report_type'])
        if 'status' in filters:
            queryset = queryset.filter(status=filters['status'])
    
    stats = {
        'total': queryset.count(),
        'by_status': dict(queryset.values('status').annotate(count=Count('id')).values_list('status', 'count')),
        'by_type': dict(queryset.values('report_type__type_code').annotate(count=Count('id')).values_list('report_type__type_code', 'count')),
        'by_priority': dict(queryset.values('priority').annotate(count=Count('id')).values_list('priority', 'count')),
    }
    
    return stats