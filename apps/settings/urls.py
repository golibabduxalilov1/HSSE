from django.urls import path
from .views import *


urlpatterns = [
    path("branches/", BranchListCreateView.as_view(), name="branch-list-create"),
    path("branches/<int:pk>/", BranchDetailView.as_view(), name="branch-detail"),
    path('departments/', DepartmentListCreateView.as_view(), name='department-list-create'),
    path("departments/<int:pk>/", DepartmentDetailView.as_view(), name="department-detail"),
    path('report-types/', ReportTypeListCreateView.as_view(), name='report-type-list'),
    path('report-types/<int:pk>/', ReportTypeDetailView.as_view(), name='report-type-detail'),
    path('risk-categories/', RiskCategoryListCreateView.as_view(), name='risk-category-list'),
    path('risk-categories/<int:pk>/', RiskCategoryDetailView.as_view(), name='risk-category-detail'),
    path('locations/', LocationListCreateView.as_view(), name='location-list'),
    path('locations/<int:pk>/', LocationDetailView.as_view(), name='location-detail'),
]
