from django.urls import path
from .views import *

urlpatterns = [
    path("", ReportListCreateView.as_view(), name="report-list-create"),
    path("<int:pk>/", ReportDetailView.as_view(), name="report-detail"),
    path(
        "<int:report_id>/fayllar/",
        ReportAttachmentCreateView.as_view(),
        name="report-attachment-create",
    ),
    path(
        "<int:report_id>/sharhlar/",
        ReportCommentCreateView.as_view(),
        name="report-comment-create",
    ),
    path("statistika/", ReportStatisticsView.as_view(), name="report-statistics"),
    path("boshqaruv-paneli/", DashboardView.as_view(), name="dashboard"),
]
