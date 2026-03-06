from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from drf_spectacular.utils import extend_schema
from django.db.models import Q
from django.utils import timezone

from .models import Conversation, Message
from .serializers import (
    ConversationSerializer,
    ConversationDetailSerializer,
    MessageSerializer,
)
from core.pagination import CustomPagination


@extend_schema(tags=["Messaging"])
class ConversationListView(generics.ListAPIView):

    serializer_class = ConversationSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ["participants__first_name", "participants__last_name"]
    ordering_fields = ["last_message_at", "created_at"]

    def get_queryset(self):
        user = self.request.user
        return (
            Conversation.objects.filter(participants=user, is_deleted=False)
            .prefetch_related("participants")
            .order_by("-last_message_at")
        )


@extend_schema(tags=["Messaging"])
class ConversationDetailView(generics.RetrieveAPIView):

    serializer_class = ConversationDetailSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Conversation.objects.filter(
            participants=user, is_deleted=False
        ).prefetch_related("participants", "messages__sender")


@extend_schema(tags=["Messaging"])
class ConversationCreateView(APIView):

    permission_classes = [IsAuthenticated]

    @extend_schema(
        request={"participant_id": "integer"}, responses={200: ConversationSerializer}
    )
    def post(self, request):
        participant_id = request.data.get("participant_id")

        if not participant_id:
            return Response(
                {"error": "participant_id majburiy"}, status=status.HTTP_400_BAD_REQUEST
            )

        conversation = (
            Conversation.objects.filter(participants=request.user)
            .filter(participants__id=participant_id)
            .first()
        )

        if conversation:
            serializer = ConversationSerializer(
                conversation, context={"request": request}
            )
            return Response(serializer.data, status=status.HTTP_200_OK)

        from apps.accounts.models import User

        try:
            participant = User.objects.get(id=participant_id)
        except User.DoesNotExist:
            return Response(
                {"error": "Foydalanuvchi topilmadi"}, status=status.HTTP_404_NOT_FOUND
            )

        conversation = Conversation.objects.create()
        conversation.participants.add(request.user, participant)

        serializer = ConversationSerializer(conversation, context={"request": request})
        return Response(serializer.data, status=status.HTTP_201_CREATED)


@extend_schema(tags=["Messaging"])
class MessageMarkAsReadView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request, message_id):
        try:
            message = Message.objects.get(id=message_id)
        except Message.DoesNotExist:
            return Response(
                {"error": "Xabar topilmadi"}, status=status.HTTP_404_NOT_FOUND
            )

        if request.user not in message.conversation.participants.all():
            return Response(
                {"error": "Sizda bu xabarni o'qish huquqi yo'q"},
                status=status.HTTP_403_FORBIDDEN,
            )

        if not message.is_read and message.sender != request.user:
            message.is_read = True
            message.read_at = timezone.now()
            message.save()

        return Response(
            {"message": "Xabar o'qilgan deb belgilandi"}, status=status.HTTP_200_OK
        )
