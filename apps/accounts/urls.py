from django.urls import path
from .views import *
urlpatterns = [
  path('register', RegisterAPiView.as_view()),
  path('varify', VerifyOTPAPIView.as_view()),
  path('login', LoginView.as_view()),

]
