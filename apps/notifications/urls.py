from django.urls import path
from .views import *

urlpatterns = [
    path("", NotificationListView.as_view(), name="notification-list"),
    # path("<int:pk>/", NotificationDetailView.as_view(), name="notification-detail"),
    # path(
    #     "<int:pk>/read/",
    #     NotificationMarkAsReadView.as_view(),
    #     name="notification-mark-read",
    # ),
    # path(
    #     "read-all/",
    #     NotificationMarkAllAsReadView.as_view(),
    #     name="notification-mark-all-read",
    # ),
    # path(
    #     "unread-count/",
    #     UnreadNotificationCountView.as_view(),
    #     name="unread-notification-count",
    # ),
]
