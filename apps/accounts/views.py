from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from drf_spectacular.utils import extend_schema
from django.core.cache import cache
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

from .models import User
from .serializers import *
from core.utils import generate_otp, send_otp_email_async
from core.exceptions import ValidationError
from .permissions import IsAdmin, IsOwnerOrAdmin
from core.pagination import CustomPagination


@extend_schema(tags=["Authentication"])
class LoginView(APIView):

    permission_classes = [AllowAny]
    serializer_class = LoginSerializer

    @extend_schema(request=LoginSerializer, responses={200: LoginSerializer})
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data.get("email")
        password = serializer.validated_data.get("password")

        user = authenticate(username=email, password=password)

        if not user:
            raise ValidationError("Email yoki parol noto'g'ri")

        if not user.is_active:
            raise ValidationError("Foydalanuvchi faol emas")

        refresh = RefreshToken.for_user(user)

        return Response(
            {
                "tokens": {
                    "access": str(refresh.access_token),
                    "refresh": str(refresh),
                },
            },
            status=status.HTTP_200_OK,
        )


@extend_schema(tags=["Authentication"])
class SendRegisterOTPView(APIView):

    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer

    @extend_schema(request=RegisterSerializer)
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data["email"]
        otp = generate_otp()

        cache.set(f"register_otp_{email}", otp, timeout=300)
        cache.set(f"register_data_{email}", serializer.validated_data, timeout=300)

        send_otp_email_async(email, otp)

        return Response(
            {"message": "6 xonali tasdiqlash kodi email pochtangizga yuborildi"},
            status=status.HTTP_200_OK,
        )


@extend_schema(tags=["Authentication"])
class VerifyOTPAndRegisterView(generics.GenericAPIView):

    permission_classes = [AllowAny]
    serializer_class = VerifyOTPSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data.get("email")
        otp = serializer.validated_data.get("otp")

        cached_otp = cache.get(f"register_otp_{email}")
        if not cached_otp or str(cached_otp) != str(otp):
            raise ValidationError("Tasdiqlash kodi noto'g'ri yoki muddati tugagan")

        cached_data = cache.get(f"register_data_{email}")
        if not cached_data:
            raise ValidationError(
                "Ro'yxatdan o'tish ma'lumotlari topilmadi. Iltimos boshidan boshlang"
            )

        password = cached_data.pop("password")
        branch_id = cached_data.pop("branch")

        user = User(**cached_data, role="employee")
        user.branch_id = branch_id
        user.set_password(password)
        user.is_active = True
        user.save()

        cache.delete(f"register_otp_{email}")
        cache.delete(f"register_data_{email}")

        return Response(
            {
                "message": "Muvaffaqiyatli ro'yxatdan o'tdingiz",
            },
            status=status.HTTP_201_CREATED,
        )


@extend_schema(tags=["Authentication"])
class RegisterView(APIView):

    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer

    @extend_schema(request=RegisterSerializer, responses={201: UserSerializer})
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        return Response(
            {
                "user": UserSerializer(user).data,
            },
            status=status.HTTP_201_CREATED,
        )


@extend_schema(tags=["Users"])
class UserListCreateView(generics.ListCreateAPIView):

    queryset = User.objects.filter(is_deleted=False)
    permission_classes = [IsAuthenticated, IsAdmin]
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["role", "branch", "department", "is_active", "gender"]
    search_fields = ["first_name", "last_name", "phone", "position"]
    ordering_fields = ["created_at", "first_name", "last_name"]

    def get_serializer_class(self):
        if self.request.method == "POST":
            return UserCreateSerializer
        return UserSerializer


@extend_schema(tags=["Users"])
class UserDetailView(generics.RetrieveUpdateDestroyAPIView):

    queryset = User.objects.filter(is_deleted=False)
    permission_classes = [IsAuthenticated, IsOwnerOrAdmin]

    def get_serializer_class(self):
        if self.request.method in ["PUT", "PATCH"]:
            return UserUpdateSerializer
        return UserSerializer

    def perform_destroy(self, instance):
        instance.delete()


@extend_schema(tags=["Users"])
class CurrentUserView(generics.RetrieveUpdateAPIView):

    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

    def get_serializer_class(self):
        if self.request.method in ["PUT", "PATCH"]:
            return UserUpdateSerializer
        return UserSerializer
