from rest_framework import generics
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema
from core.utils import generate_otp, send_otp_email_async
from rest_framework.permissions import AllowAny
from django.core.cache import cache
from rest_framework.response import Response
from django.contrib.auth import get_user_model
User = get_user_model()
from django.core.exceptions import ValidationError

# local
from .models import User
from .serializers import RegisterSerializer, VerifyOtpSerializer, LoginSerializers


class RegisterAPiView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer

    def perform_create(self, serializer):
        user = serializer.save()

        otp = generate_otp()

        cache.set(f"otp_{user.email}", otp, timeout=60)

        cache.set(f"otp_session_{otp}", user.email, timeout=60)

        send_otp_email_async(user.email, otp)


class VerifyOTPAPIView(APIView):
    permission_classes = [AllowAny]
    serializer_class = VerifyOtpSerializer

    def post(self, request):

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        otp = serializer.validated_data["otp"]
        email = cache.get(f"otp_session_{otp}")
        if not email:
            return Response(
                {"error": "OTP eskirgan yoki noto‘g‘ri"},
                status=400
            )
        cached_otp = cache.get(f"otp_{email}")
        if cached_otp != otp:
            return Response(
                {"error": "OTP noto‘g‘ri"},
                status=400
            )
        user = User.objects.get(email=email)
        user.is_active = True
        user.save(update_fields=["is_active"])

        cache.delete(f"otp_{email}")
        cache.delete(f"otp_session_{otp}")

        return Response({
            "message": "Account tasdiqlandi"
        })

class LoginView(APIView):
    permission_classes = [AllowAny]
    serializer_class = LoginSerializers

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.validated_data)