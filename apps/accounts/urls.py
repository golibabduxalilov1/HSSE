from django.urls import path
from .views import *
<<<<<<< HEAD
urlpatterns = [
  path('register', RegisterAPiView.as_view()),
  path('varify', VerifyOTPAPIView.as_view()),
  path('login', LoginView.as_view()),

]
=======

urlpatterns = [
    # Auth
    path('login/', LoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    
    # Users
    path('users/', UserListCreateView.as_view(), name='user-list-create'),
    path('users/<int:pk>/', UserDetailView.as_view(), name='user-detail'),
    path('me/', CurrentUserView.as_view(), name='current-user'),
]
>>>>>>> fbf1b5d (Complete BranchDetailView and Change Accounts)
