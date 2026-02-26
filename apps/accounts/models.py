from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from core.mixins import TimeStampedMixin, SoftDeleteMixin
from core.utils import get_file_path


class UserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email majburiy")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("role", "superadmin")
        return self.create_user(email, password, **extra_fields)


class User(AbstractUser, TimeStampedMixin, SoftDeleteMixin):

    ROLE_CHOICES = (
        ("superadmin", "Super Admin"),
        ("admin", "Admin"),
        ("employee", "Employee"),
    )
    GENDER_CHOICES = (
        ("male", "Erkak"),
        ("female", "Ayol"),
    )

    username = None
    email = models.EmailField(unique=True, verbose_name="Email")

    full_name = models.CharField(max_length=100, verbose_name="Ism va familiya")
    phone = models.CharField(
        max_length=20, null=True, blank=True, verbose_name="Telefon raqam"
    )
    birth_date = models.DateField(null=True, blank=True, verbose_name="Tug'ilgan sana")
    gender = models.CharField(
        max_length=10, choices=GENDER_CHOICES, verbose_name="Jinsi"
    )
    avatar = models.ImageField(
        upload_to=get_file_path, null=True, blank=True, verbose_name="Profil rasmi"
    )

    role = models.CharField(
        max_length=20, choices=ROLE_CHOICES, default="employee", verbose_name="Rol"
    )
    position = models.CharField(
        max_length=200, null=True, blank=True, verbose_name="Lavozim"
    )
    branch = models.ForeignKey(
        "settings.Branch",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="users",
    )
    department = models.ForeignKey(
        "settings.Department",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="users",
    )

    is_active = models.BooleanField(default=False, verbose_name="Faol")

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["full_name"]

    class Meta:
        db_table = "users"
        verbose_name = "Foydalanuvchi"
        verbose_name_plural = "Foydalanuvchilar"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.full_name} "

    def is_superadmin(self):
        return self.role == "superadmin"

    def is_admin(self):
        return self.role in ["superadmin", "admin"]

    def is_employee(self):
        return self.role == "employee"
