from drf_spectacular.utils import extend_schema, OpenApiResponse
from rest_framework import status
from rest_framework.generics import CreateAPIView, RetrieveAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from users.serializers import UserRegistrationSerializer, UserLoginSerializer
from users.services import UserAuthService, FernetService


class UserRegistrationAPIView(CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = UserRegistrationSerializer

    @extend_schema(
        responses={201: OpenApiResponse(description='{"access_token": "Your access Token"}')})
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        access_token = UserAuthService.create_user(serializer.validated_data)
        return Response(data={"access_token": access_token}, status=status.HTTP_201_CREATED)


class UserLoginAPIView(CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = UserLoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        access_token = UserAuthService.login_user(serializer.validated_data)
        return Response(data={"access_token": access_token}, status=status.HTTP_200_OK)


class UserChatTokenAPIView(RetrieveAPIView):

    @extend_schema(
        responses={200: OpenApiResponse(description='{"token": "Your Telegram Token"}')})
    def get(self, request, *args, **kwargs):
        token = FernetService.generate_token(username=request.user.username)
        return Response({"token": token}, status=status.HTTP_200_OK)
