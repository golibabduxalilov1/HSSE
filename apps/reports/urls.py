from django.urls import path
from .views import *

urlpatterns = [
    path('', ReportListCreateView.as_view(), name='report-list-create'),
    path('<int:pk>/', ReportDetailView.as_view(), name='report-detail'),
    
    path('<int:report_id>/attachments/', ReportAttachmentCreateView.as_view(), name='report-attachment-create'),
    
    path('<int:report_id>/comments/', ReportCommentCreateView.as_view(), name='report-comment-create'),
    
    path('statistics/', ReportStatisticsView.as_view(), name='report-statistics'),
    
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
]