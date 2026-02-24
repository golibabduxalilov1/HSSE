from rest_framework import serializers
from .models import User
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate


from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from .models import User


class RegisterSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            "full_name",
            "email",
            "department",
            "password",
            "password2",
        ]

    def validate(self, attrs):
        if attrs["password"] != attrs["password2"]:
            raise serializers.ValidationError(
                {"password": "Parollar mos emas"}
            )
        validate_password(attrs["password"])
        if User.objects.filter(email=attrs["email"]).exists():
            raise serializers.ValidationError({
                "email": "Bu email mavjud"
            })

        names = attrs["full_name"].strip().split()

        if len(names) < 2:
            raise serializers.ValidationError(
                {"full_name": "Ism va familiya kiriting"}
            )

        return attrs

    def create(self, validated_data):
        validated_data.pop("password2")

        full_name = validated_data.pop("full_name")
        names = full_name.strip().split()

        first_name = names[0]
        last_name = " ".join(names[1:])

        user = User.objects.create_user(
            first_name=first_name,
            last_name=last_name,
            is_active=False,
            **validated_data
        )

        return user

class VerifyOtpSerializer(serializers.Serializer):
    otp = serializers.CharField(max_length=6)

class LoginSerializers(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")

        user = authenticate(
            username=email,
            password=password
        )

        if not user:
            raise serializers.ValidationError(
                "Email yoki parol noto‘g‘ri"
            )

        if not user.is_active:
            raise serializers.ValidationError(
                "Account tasdiqlanmagan"
            )

        refresh = RefreshToken.for_user(user)

        return {
            "access": str(refresh.access_token),
            "refresh": str(refresh),
            "user": {
                "id": user.id,
                "email": user.email,
                "full_name": user.full_name,
                "role": user.role,
            }
        }