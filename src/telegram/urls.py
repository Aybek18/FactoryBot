from django.urls import path

from telegram.views import ListMessagesView, MessageSendAPIView

urlpatterns = [
    path("", ListMessagesView.as_view(), name="message-list"),
    path("send/", MessageSendAPIView.as_view(), name="message-send"),
]
