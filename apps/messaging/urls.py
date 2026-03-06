from django.urls import path
from .views import *

urlpatterns = [
    path("conversations/", ConversationListView.as_view(), name="conversation-list"),
    path(
        "conversations/create/",
        ConversationCreateView.as_view(),
        name="conversation-create",
    ),
    path(
        "conversations/<int:pk>/",
        ConversationDetailView.as_view(),
        name="conversation-detail",
    ),
    path(
        "messages/<int:message_id>/read/",
        MessageMarkAsReadView.as_view(),
        name="message-mark-read",
    ),
]
