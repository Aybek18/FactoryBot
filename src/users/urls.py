from django.urls import path

from users.views import UserRegistrationAPIView, UserLoginAPIView, UserChatTokenAPIView

urlpatterns = [
    path("login", UserLoginAPIView.as_view(), name="user-login"),
    path("registration/", UserRegistrationAPIView.as_view(), name="user-registration"),
    path("generate-token", UserChatTokenAPIView.as_view(), name="user-chat-token")
]