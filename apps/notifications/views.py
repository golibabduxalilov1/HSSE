from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from drf_spectacular.utils import extend_schema
from django.utils import timezone

from .models import Notification
from .serializers import NotificationSerializer, NotificationListSerializer
from core.pagination import CustomPagination


@extend_schema(tags=["Notifications"])
class NotificationListView(generics.ListAPIView):

    serializer_class = NotificationListSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ["notification_type", "is_read"]
    ordering_fields = ["created_at"]

    def get_queryset(self):
        user = self.request.user

        if not user.is_authenticated:
            return Notification.objects.none()

        return (
            Notification.objects.filter(recipient=user)
            .select_related("sender", "report")
            .order_by("-created_at")
        )
