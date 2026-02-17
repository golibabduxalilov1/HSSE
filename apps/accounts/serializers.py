from rest_framework import serializers
from django.core.cache import cache
from .models import User
from core.utils import generate_unique_code
import threading
from django.core.mail import send_mail
from django.conf import settings


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            "email",
            "first_name",
            "last_name",
            "phone",
            "birth_date",
            "gender",
            "avatar",
            "position",
            "role",
            "branch",
            "department",
            "password",
            "password2",
        ]

    def validate(self, attrs):
        try:
            if attrs["password"] != attrs["password2"]:
                raise serializers.ValidationError("Parollar mos emas")

            if User.objects.filter(email=attrs["email"]).exists():
                raise serializers.ValidationError("Email mavjud")

            return attrs

        except KeyError:
            raise serializers.ValidationError("Kerakli maydonlar yuborilmadi")

        except Exception as e:
            raise serializers.ValidationError(str(e))

    def create(self, validated_data):
        try:
            validated_data.pop("password2")
            password = validated_data.pop("password")

            user = User(**validated_data)
            user.set_password(password)
            user.is_active = False
            user.save()

            otp = generate_unique_code(length=6)

            cache.set(
                f"verify_{user.email}",
                otp,
                timeout=300,
            )

            def send_email_async():
                try:
                    send_mail(
                        subject="Tasdiqlash kodi",
                        message=f"Sizning tasdiqlash kodingiz: {otp}",
                        from_email=settings.DEFAULT_FROM_EMAIL,
                        recipient_list=[user.email],
                        fail_silently=False,
                    )
                except Exception as e:
                    print("EMAIL ERROR:", e)

            threading.Thread(
                target=send_email_async,
                daemon=True
            ).start()

            return user

        except Exception as e:
            raise serializers.ValidationError(
                {"detail": f"User yaratishda xatolik: {str(e)}"}
            )

class VerifyOTPSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField()

    def validate(self, attrs):
        try:
            email = attrs.get("email")
            otp = attrs.get("otp")

            cached_otp = cache.get(f"verify_{email}")

            if cached_otp is None:
                raise serializers.ValidationError(
                    "OTP muddati tugagan yoki yuborilmagan"
                )

            if str(cached_otp) != str(otp):
                raise serializers.ValidationError("OTP xato")

            return attrs

        except Exception as e:
            raise serializers.ValidationError(str(e))

    def save(self):
        try:
            email = self.validated_data["email"]

            user = User.objects.get(email=email)
            user.is_active = True
            user.save()

            cache.delete(f"verify_{email}")

            return user

        except User.DoesNotExist:
            raise serializers.ValidationError("Foydalanuvchi topilmadi")

        except Exception as e:
            raise serializers.ValidationError(
                {"detail": f"OTP tasdiqlashda xatolik: {str(e)}"}
            )
