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


@extend_schema(tags=["Bildirishnomalar"])
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


@extend_schema(tags=["Bildirishnomalar"])
class NotificationDetailView(generics.RetrieveAPIView):

    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Notification.objects.filter(recipient=user).select_related(
            "sender", "report"
        )

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()

        # Mark as read
        if not instance.is_read:
            instance.is_read = True
            instance.read_at = timezone.now()
            instance.save()

        serializer = self.get_serializer(instance)
        return Response(serializer.data)


@extend_schema(tags=["Bildirishnomalar"])
class NotificationMarkAsReadView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        try:
            notification = Notification.objects.get(id=pk, recipient=request.user)
        except Notification.DoesNotExist:
            return Response(
                {"error": "Bildirishnoma topilmadi"}, status=status.HTTP_404_NOT_FOUND
            )

        if not notification.is_read:
            notification.is_read = True
            notification.read_at = timezone.now()
            notification.save()

        return Response(
            {"message": "Bildirishnoma o'qilgan deb belgilandi"},
            status=status.HTTP_200_OK,
        )


@extend_schema(tags=["Bildirishnomalar"])
class NotificationMarkAllAsReadView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):
        Notification.objects.filter(recipient=request.user, is_read=False).update(
            is_read=True, read_at=timezone.now()
        )

        return Response(
            {"message": "Barcha bildirishnomalar o'qilgan deb belgilandi"},
            status=status.HTTP_200_OK,
        )


@extend_schema(tags=["Bildirishnomalar"])
class UnreadNotificationCountView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        count = Notification.objects.filter(
            recipient=request.user, is_read=False
        ).count()

        return Response({"count": count}, status=status.HTTP_200_OK)
