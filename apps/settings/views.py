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