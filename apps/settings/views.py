from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from drf_spectacular.utils import extend_schema

from .models import Branch, Location, Department, ReportType, RiskCategory
from .serializers import (
    BranchSerializer, LocationSerializer, DepartmentSerializer,
    ReportTypeSerializer, RiskCategorySerializer
)
from .permissions import IsSuperAdminOrReadOnly
from core.pagination import CustomPagination


@extend_schema(tags=['Settings - Branches'])
class BranchListCreateView(generics.ListCreateAPIView):

    queryset = Branch.objects.filter(is_deleted=False)
    serializer_class = BranchSerializer
    permission_classes = [IsAuthenticated, IsSuperAdminOrReadOnly]
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['status']
    search_fields = ['name', 'address']
    ordering_fields = ['name', 'created_at']


@extend_schema(tags=['Settings - Branches'])
class BranchDetailView(generics.RetrieveUpdateDestroyAPIView):

    queryset = Branch.objects.filter(is_deleted=False)
    serializer_class = BranchSerializer
    permission_classes = [IsAuthenticated, IsSuperAdminOrReadOnly]

    def perform_destroy(self, instance):
        instance.delete()

@extend_schema(tags=['Settings - Departments'])
class DepartmentListCreateView(generics.ListCreateAPIView):
    queryset = Department.objects.filter(is_deleted=False)
    serializer_class = DepartmentSerializer
    permission_classes = [IsAuthenticated, IsSuperAdminOrReadOnly]
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['status']
    search_fields = ['name']
    ordering_fields = ['name', 'created_at']

@extend_schema(tags=['Settings - Departments'])
class DepartmentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Department.objects.filter(is_deleted=False)
    serializer_class = DepartmentSerializer
    permission_classes = [IsAuthenticated, IsSuperAdminOrReadOnly]

    def perform_destroy(self, instance):
        instance.is_deleted = True
        instance.save()

@extend_schema(tags=['Settings - ReportType'])
class ReportTypeListCreateView(generics.ListCreateAPIView):
    queryset = ReportType.objects.all()
    serializer_class = ReportTypeSerializer
    permission_classes = [IsAuthenticated, IsSuperAdminOrReadOnly]
    pagination_class = CustomPagination
    filterset_fields = ['status']
    search_fields = ['name']
    ordering_fields = ['name', 'created_at']

@extend_schema(tags=['Settings - ReportType'])
class ReportTypeDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ReportType.objects.all()
    serializer_class = ReportTypeSerializer
    permission_classes = [IsAuthenticated, IsSuperAdminOrReadOnly]

@extend_schema(tags=['Settings - RiskCategory'])
class RiskCategoryListCreateView(generics.ListCreateAPIView):
    queryset = RiskCategory.objects.all()
    serializer_class = RiskCategorySerializer
    permission_classes = [IsAuthenticated, IsSuperAdminOrReadOnly]
    pagination_class = CustomPagination


@extend_schema(tags=['Settings - RiskCategory'])
class RiskCategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = RiskCategory.objects.all()
    serializer_class = RiskCategorySerializer
    permission_classes = [IsAuthenticated, IsSuperAdminOrReadOnly]


@extend_schema(tags=['Settings - Location'])
class LocationListCreateView(generics.ListCreateAPIView):
    queryset = Location.objects.filter(is_deleted=False).select_related('branch')
    serializer_class = LocationSerializer
    permission_classes = [IsAuthenticated, IsSuperAdminOrReadOnly]
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['status', 'branch']
    search_fields = ['name', 'branch__name']
    ordering_fields = ['name', 'created_at']


@extend_schema(tags=['Settings - Location'])
class LocationDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Location.objects.filter(is_deleted=False).select_related('branch')
    serializer_class = LocationSerializer
    permission_classes = [IsAuthenticated, IsSuperAdminOrReadOnly]

    def perform_destroy(self, instance):
        instance.is_deleted = True
        instance.save()