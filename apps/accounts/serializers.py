from rest_framework import serializers
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User
from core.exceptions import ValidationError


class UserSerializer(serializers.ModelSerializer):
    branch_name = serializers.CharField(source="branch.name", read_only=True)
    department_name = serializers.CharField(source="department.name", read_only=True)

    class Meta:
        model = User
        fields = [
            "id",
            "full_name",
            "email",
            "phone",
            "birth_date",
            "gender",
            "avatar",
            "role",
            "position",
            "branch",
            "branch_name",
            "department",
            "department_name",
            "is_active",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]


class UserCreateSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "phone",
            "password",
            "birth_date",
            "gender",
            "role",
            "position",
            "branch",
            "department",
        ]

    def validate_phone(self, value):
        if User.objects.filter(phone=value).exists():
            raise ValidationError("Bu telefon raqam allaqachon ro'yxatdan o'tgan")
        return value

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


class UserUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "birth_date",
            "gender",
            "avatar",
            "position",
            "branch",
            "department",
        ]


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True, write_only=True)


class LoginSerializers(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")

        # authenticate username kutadi, User modelida USERNAME_FIELD = "email"
        user = authenticate(username=email, password=password)

        if not user:
            raise ValidationError("Email yoki parol noto'g'ri")

        if not user.is_active:
            raise ValidationError("Foydalanuvchi faol emas")

        refresh = RefreshToken.for_user(user)

        return {
            "user": UserSerializer(user).data,
            "tokens": {
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            },
        }


class RegisterSerializer(serializers.Serializer):
    full_name = serializers.CharField(required=True)
    branch = serializers.IntegerField(required=True)
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True, write_only=True, min_length=8)
    password2 = serializers.CharField(required=True, write_only=True, min_length=8)

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise ValidationError("Bu email allaqachon ro'yxatdan o'tgan")
        return value

    def validate(self, data):
        if data["password"] != data["password2"]:
            raise ValidationError("Passwordlar mos emas!")

        data.pop("password2")
        return data


class VerifyOTPSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    otp = serializers.CharField(required=True, max_length=6)
