<<<<<<< HEAD
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
=======
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from drf_spectacular.utils import extend_schema, OpenApiParameter
>>>>>>> fbf1b5d (Complete BranchDetailView and Change Accounts)

from .models import User
<<<<<<< HEAD
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
=======
from .serializers import *
from .permissions import IsAdmin, IsOwnerOrAdmin
from core.pagination import CustomPagination


@extend_schema(tags=['Authentication'])
class LoginView(APIView):
    
    permission_classes = [AllowAny]
    serializer_class = LoginSerializer
    
    @extend_schema(
        request=LoginSerializer,
        responses={200: LoginSerializer}
    )
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.validated_data, status=status.HTTP_200_OK)


@extend_schema(tags=['Authentication'])
class RegisterView(APIView):
    
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer
    
    @extend_schema(
        request=RegisterSerializer,
        responses={201: UserSerializer}
    )
    def post(self, request):
        try:
            serializer = RegisterSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            user = serializer.save()
            
            refresh = RefreshToken.for_user(user)
            
            return Response({
                'user': UserSerializer(user).data,
                'tokens': {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                }
            }, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)






@extend_schema(tags=['Users'])
class UserListCreateView(generics.ListCreateAPIView):
    
    queryset = User.objects.filter(is_deleted=False)
    permission_classes = [IsAuthenticated, IsAdmin]
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['role', 'branch', 'department', 'is_active', 'gender']
    
    search_fields = ['full_name', 'email', 'phone', 'position']
    ordering_fields = ['created_at', 'full_name']
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return UserCreateSerializer
        return UserSerializer
    
@extend_schema(tags=['Users'])
class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    """User detail, update and delete view"""
    
    queryset = User.objects.filter(is_deleted=False)
    permission_classes = [IsAuthenticated, IsOwnerOrAdmin]
    
    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return UserUpdateSerializer
        return UserSerializer
    
    def perform_destroy(self, instance):
        instance.delete()


@extend_schema(tags=['Users'])
class CurrentUserView(generics.RetrieveUpdateAPIView):
    """Current user view"""
    
    permission_classes = [IsAuthenticated]
    
    def get_object(self):
        return self.request.user
    
    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return UserUpdateSerializer
        return UserSerializer


>>>>>>> fbf1b5d (Complete BranchDetailView and Change Accounts)
