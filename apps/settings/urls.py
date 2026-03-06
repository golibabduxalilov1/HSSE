from django.urls import path
from .views import *


urlpatterns = [
    path("filiallar/", BranchListCreateView.as_view(), name="branch-list-create"),
    path("filiallar/<int:pk>/", BranchDetailView.as_view(), name="branch-detail"),
    path(
        "bolimlar/", DepartmentListCreateView.as_view(), name="department-list-create"
    ),
    path(
        "bolimlar/<int:pk>/", DepartmentDetailView.as_view(), name="department-detail"
    ),
    path(
        "hisobot-turlari/", ReportTypeListCreateView.as_view(), name="report-type-list"
    ),
    path(
        "hisobot-turlari/<int:pk>/",
        ReportTypeDetailView.as_view(),
        name="report-type-detail",
    ),
    path(
        "xavf-turlari/",
        RiskCategoryListCreateView.as_view(),
        name="risk-category-list",
    ),
    path(
        "xavf-turlari/<int:pk>/",
        RiskCategoryDetailView.as_view(),
        name="risk-category-detail",
    ),
    path("manzillar/", LocationListCreateView.as_view(), name="location-list"),
    path("manzillar/<int:pk>/", LocationDetailView.as_view(), name="location-detail"),
]
