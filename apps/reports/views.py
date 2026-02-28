from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from drf_spectacular.utils import extend_schema
from django.db.models import Count, Q
from django.utils import timezone
from datetime import timedelta

from .models import Report, ReportAttachment, ReportComment, ReportHistory
from .serializers import *
from .filters import ReportFilter
from .permissions import *
from core.pagination import CustomPagination
from apps.settings.models import ReportType


@extend_schema(tags=["Reports - Hisobotlar"])
class ReportListCreateView(generics.ListCreateAPIView):

    permission_classes = [IsAuthenticated, CanCreateReport]
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = ReportFilter
    search_fields = ["code", "title", "description"]
    ordering_fields = ["created_at", "deadline", "status", "priority"]

    def get_queryset(self):
        user = self.request.user
        queryset = Report.objects.filter(is_deleted=False).select_related(
            "report_type", "branch", "location", "reporter", "assignee"
        )

        if user.is_admin():
            return queryset

        return queryset.filter(Q(reporter=user) | Q(assignee=user))

    def get_serializer_class(self):
        if self.request.method == "POST":
            return ReportCreateSerializer
        return ReportListSerializer


@extend_schema(tags=["Reports - Hisobotlar"])
class ReportDetailView(generics.RetrieveUpdateDestroyAPIView):

    queryset = (
        Report.objects.filter(is_deleted=False)
        .select_related(
            "report_type", "risk_category", "branch", "location", "reporter", "assignee"
        )
        .prefetch_related("attachments", "comments", "history")
    )

    def get_permissions(self):
        if self.request.method == "GET":
            return [IsAuthenticated(), CanViewReport()]
        elif self.request.method in ["PUT", "PATCH"]:
            return [IsAuthenticated(), CanEditReport()]
        elif self.request.method == "DELETE":
            return [IsAuthenticated(), CanDeleteReport()]
        return [IsAuthenticated()]

    def get_serializer_class(self):
        if self.request.method in ["PUT", "PATCH"]:
            return ReportUpdateSerializer
        return ReportDetailSerializer

    def perform_destroy(self, instance):
        instance.delete()


@extend_schema(tags=["Reports - Hisobotlar"])
class ReportAttachmentCreateView(generics.CreateAPIView):

    serializer_class = ReportAttachmentSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        report_id = self.kwargs.get("report_id")
        report = Report.objects.get(id=report_id)

        user = self.request.user
        if not (user.is_admin() or report.reporter == user or report.assignee == user):
            from core.exceptions import PermissionDenied

            raise PermissionDenied("Sizda bu hisobotga fayl yuklash huquqi yo'q")

        serializer.save(report=report)


@extend_schema(tags=["Reports - Hisobotlar"])
class ReportCommentCreateView(generics.CreateAPIView):

    serializer_class = ReportCommentSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        report_id = self.kwargs.get("report_id")
        report = Report.objects.get(id=report_id)

        user = self.request.user
        if not (user.is_admin() or report.reporter == user or report.assignee == user):
            from core.exceptions import PermissionDenied

            raise PermissionDenied("Sizda bu hisobotga sharh qoldirish huquqi yo'q")

        serializer.save(report=report, user=user)


@extend_schema(tags=["Reports - Statistika"])
class ReportStatisticsView(APIView):

    permission_classes = [IsAuthenticated]

    @extend_schema(responses={200: ReportStatisticsSerializer})
    def get(self, request):
        user = request.user

        if user.is_admin():
            queryset = Report.objects.filter(is_deleted=False)
        else:
            queryset = Report.objects.filter(
                Q(reporter=user) | Q(assignee=user), is_deleted=False
            )

        branch_id = request.query_params.get("branch")
        report_type_id = request.query_params.get("report_type")
        date_from = request.query_params.get("date_from")
        date_to = request.query_params.get("date_to")

        if branch_id:
            queryset = queryset.filter(branch_id=branch_id)
        if report_type_id:
            queryset = queryset.filter(report_type_id=report_type_id)
        if date_from:
            queryset = queryset.filter(created_at__gte=date_from)
        if date_to:
            queryset = queryset.filter(created_at__lte=date_to)

        total_reports = queryset.count()
        new_reports = queryset.filter(status="new").count()
        in_progress_reports = queryset.filter(status="in_progress").count()
        completed_reports = queryset.filter(status="completed").count()
        cancelled_reports = queryset.filter(status="cancelled").count()

        nearmiss_count = queryset.filter(report_type__type_code="nearmiss").count()
        observation_count = queryset.filter(
            report_type__type_code="observation"
        ).count()
        accident_count = queryset.filter(report_type__type_code="accident").count()
        incident_count = queryset.filter(report_type__type_code="incident").count()

        by_status = dict(
            queryset.values("status")
            .annotate(count=Count("id"))
            .values_list("status", "count")
        )

        by_type = dict(
            queryset.values("report_type__type_code")
            .annotate(count=Count("id"))
            .values_list("report_type__type_code", "count")
        )

        by_priority = dict(
            queryset.values("priority")
            .annotate(count=Count("id"))
            .values_list("priority", "count")
        )

        by_branch = dict(
            queryset.values("branch__name")
            .annotate(count=Count("id"))
            .values_list("branch__name", "count")
        )

        monthly_stats = {}
        for i in range(12):
            month_start = timezone.now() - timedelta(days=30 * i)
            month_end = month_start + timedelta(days=30)
            month_name = month_start.strftime("%b")
            count = queryset.filter(
                created_at__gte=month_start, created_at__lt=month_end
            ).count()
            monthly_stats[month_name] = count

        data = {
            "total_reports": total_reports,
            "new_reports": new_reports,
            "in_progress_reports": in_progress_reports,
            "completed_reports": completed_reports,
            "cancelled_reports": cancelled_reports,
            "nearmiss_count": nearmiss_count,
            "observation_count": observation_count,
            "accident_count": accident_count,
            "incident_count": incident_count,
            "by_status": by_status,
            "by_type": by_type,
            "by_priority": by_priority,
            "by_branch": by_branch,
            "monthly_stats": monthly_stats,
        }

        serializer = ReportStatisticsSerializer(data)
        return Response(serializer.data, status=status.HTTP_200_OK)


@extend_schema(tags=["Reports - Boshqaruv paneli"])
class DashboardView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        if user.is_admin():
            queryset = Report.objects.filter(is_deleted=False)
        else:
            queryset = Report.objects.filter(
                Q(reporter=user) | Q(assignee=user), is_deleted=False
            )

        report_types = ReportType.objects.filter(is_deleted=False, status="active")
        report_type_stats = []

        for rt in report_types:
            count = queryset.filter(report_type=rt).count()
            total = queryset.count()
            percentage = (count / total * 100) if total > 0 else 0

            report_type_stats.append(
                {
                    "name": rt.name,
                    "type_code": rt.type_code,
                    "count": count,
                    "percentage": round(percentage, 1),
                }
            )

        recent_reports = queryset.order_by("-created_at")[:5]
        recent_reports_data = ReportListSerializer(recent_reports, many=True).data

        if user.is_employee():
            pending_assignments = queryset.filter(
                assignee=user, status__in=["new", "in_progress"]
            ).count()
        else:
            pending_assignments = queryset.filter(status="new").count()

        data = {
            "report_type_stats": report_type_stats,
            "recent_reports": recent_reports_data,
            "pending_assignments": pending_assignments,
            "total_reports": queryset.count(),
        }

        return Response(data, status=status.HTTP_200_OK)
