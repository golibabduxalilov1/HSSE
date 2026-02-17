from django.urls import path
from .views import RegisterCreateApiView, VerifyOtpView
urlpatterns = [
  path('register', RegisterCreateApiView.as_view()),
  path('login', VerifyOtpView.as_view())
]
