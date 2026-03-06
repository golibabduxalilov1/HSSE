from django.urls import path
from .views import *

urlpatterns = [
    path("suhbatlar/", ConversationListView.as_view(), name="conversation-list"),
    path(
        "suhbatlar/yaratish/",
        ConversationCreateView.as_view(),
        name="conversation-create",
    ),
    path(
        "suhbatlar/<int:pk>/",
        ConversationDetailView.as_view(),
        name="conversation-detail",
    ),
    path(
        "xabarlar/<int:message_id>/o'qildi/",
        MessageMarkAsReadView.as_view(),
        name="message-mark-read",
    ),
]
