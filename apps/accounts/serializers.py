from rest_framework import serializers
<<<<<<< HEAD
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
=======
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User
from core.exceptions import ValidationError


class UserSerializer(serializers.ModelSerializer):
    
    # branch_name = serializers.CharField(source='branch.name', read_only=True)
    department_name = serializers.CharField(source='department.name', read_only=True)
    
    class Meta:
        model = User
        fields = [
            'id', 'full_name', 'phone', 'email',
            'birth_date', 'gender', 'avatar', 'role', 'position',
            'branch', 'branch_name', 'department', 'department_name',
            'is_active', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class UserCreateSerializer(serializers.ModelSerializer):
    
    password = serializers.CharField(write_only=True, min_length=8)
    
    class Meta:
        model = User
        fields = [
            'full_name', 'email', 'phone', 'password',
            'birth_date', 'gender', 'role', 'position',
            'branch', 'department'
        ]
    
    def validate_phone(self, value):
        if value and User.objects.filter(phone=value).exists():
            raise ValidationError('Bu telefon raqam allaqachon ro\'yxatdan o\'tgan')
        return value
    
    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


class UserUpdateSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = [
            'full_name', 'email', 'phone', 'birth_date', 'gender',
            'avatar', 'position', 'branch', 'department', 'is_active'
>>>>>>> fbf1b5d (Complete BranchDetailView and Change Accounts)
        ]


class LoginSerializer(serializers.Serializer):
    
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True, write_only=True)
    
    def validate(self, attrs):
<<<<<<< HEAD
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
=======
        email = attrs.get('email')
        password = attrs.get('password')
        
        user = authenticate(username=email, password=password)
        
        if not user:
            raise ValidationError('Email yoki parol noto\'g\'ri')
        
        if not user.is_active:
            raise ValidationError('Foydalanuvchi faol emas')
        
        refresh = RefreshToken.for_user(user)
        
        return {
            'user': UserSerializer(user).data,
            'tokens': {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
        }


class RegisterSerializer(serializers.Serializer):
    
    full_name = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)
    phone = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True, min_length=8)
    birth_date = serializers.DateField(required=False)
    gender = serializers.ChoiceField(choices=User.GENDER_CHOICES, required=True)
    branch = serializers.IntegerField(required=True)
    
    def validate_phone(self, value):
        if User.objects.filter(phone=value).exists():
            raise ValidationError('Bu telefon raqam allaqachon ro\'yxatdan o\'tgan')
        return value
>>>>>>> fbf1b5d (Complete BranchDetailView and Change Accounts)

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise ValidationError('Bu email allaqachon ro\'yxatdan o\'tgan')
        return value
    
    def create(self, validated_data):
<<<<<<< HEAD
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
=======
        password = validated_data.pop('password')
        user = User(**validated_data, role='employee')
        user.set_password(password)
        user.save()
        return user
>>>>>>> fbf1b5d (Complete BranchDetailView and Change Accounts)
