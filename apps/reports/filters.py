from django_filters import rest_framework as filters
from .models import Report


class ReportFilter(filters.FilterSet):

    created_at_from = filters.DateFilter(field_name="created_at", lookup_expr="gte")
    created_at_to = filters.DateFilter(field_name="created_at", lookup_expr="lte")
    deadline_from = filters.DateFilter(field_name="deadline", lookup_expr="gte")
    deadline_to = filters.DateFilter(field_name="deadline", lookup_expr="lte")

    class Meta:
        model = Report
        fields = {
            "status": ["exact", "in"],
            "priority": ["exact", "in"],
            "report_type": ["exact"],
            "branch": ["exact"],
            "location": ["exact"],
            "reporter": ["exact"],
            "assignee": ["exact"],
            "is_anonymous": ["exact"],
        }
