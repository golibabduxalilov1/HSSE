from django.urls import path
from .views import *

urlpatterns = [
    path("kirish/", LoginView.as_view(), name="login"),
    path("royxatdan-otish/", SendRegisterOTPView.as_view(), name="register-send-otp"),
    path(
        "royxatdan-otish/tasdiqlash/",
        VerifyOTPAndRegisterView.as_view(),
        name="register-verify",
    ),
    # Foydalanuvchilar bilan ishlash
    path("foydalanuvchilar/", UserListCreateView.as_view(), name="user-list-create"),
    path("foydalanuvchilar/<int:pk>/", UserDetailView.as_view(), name="user-detail"),
    # Profil
    path("profilim/", CurrentUserView.as_view(), name="current-user"),
]
