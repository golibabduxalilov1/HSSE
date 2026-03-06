from django.urls import path
from .views import *

urlpatterns = [
    path("", NotificationListView.as_view(), name="notification-list"),
    path("<int:pk>/", NotificationDetailView.as_view(), name="notification-detail"),
    path(
        "<int:pk>/o'qildi/",
        NotificationMarkAsReadView.as_view(),
        name="notification-mark-read",
    ),
    path(
        "barchasini-o'qildi-deb-belgilash/",
        NotificationMarkAllAsReadView.as_view(),
        name="notification-mark-all-read",
    ),
    path(
        "o'qilmaganlar-soni/",
        UnreadNotificationCountView.as_view(),
        name="unread-notification-count",
    ),
]
