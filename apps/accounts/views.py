from django.shortcuts import render
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

# local
from .models import User
from .serializers import RegisterSerializer, VerifyOTPSerializer


class RegisterCreateApiView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        try:
            serializer = self.serializer_class(data=request.data)
            serializer.is_valid(raise_exception=True)

            user = serializer.save()

            return Response({
                "message": "OTP yuborildi",
                "status": status.HTTP_201_CREATED,
                "role": user.role
            }, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({
                "error": str(e),
                "status": status.HTTP_400_BAD_REQUEST
            }, status=status.HTTP_400_BAD_REQUEST)


class VerifyOtpView(generics.GenericAPIView):
    serializer_class = VerifyOTPSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            user = serializer.save()

            refresh = RefreshToken.for_user(user)

            return Response({
                "refresh": str(refresh),
                "access": str(refresh.access_token),
                "message": "Profilingiz muvaffaqiyatli faollashtirildi",
                "role": user.role,
                "status": status.HTTP_200_OK
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({
                "error": str(e),
                "status": status.HTTP_400_BAD_REQUEST
            }, status=status.HTTP_400_BAD_REQUEST)
