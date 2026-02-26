from django.urls import path
from .views import *

urlpatterns = [
    # Auth
    path("login/", LoginView.as_view(), name="login"),
    path("register/", SendRegisterOTPView.as_view(), name="register-send-otp"),
    path(
        "register/verify/", VerifyOTPAndRegisterView.as_view(), name="register-verify"
    ),
    path("users/", UserListCreateView.as_view(), name="user-list-create"),
    path("users/<int:pk>/", UserDetailView.as_view(), name="user-detail"),
    path("me/", CurrentUserView.as_view(), name="current-user"),
]
