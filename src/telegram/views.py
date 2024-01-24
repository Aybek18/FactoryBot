from rest_framework import status
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.response import Response

from telegram.models import TelegramMessage
from telegram.serializers import TelegramMessageSerializer
from telegram.services import TelegramService


class ListMessagesView(ListAPIView):
    serializer_class = TelegramMessageSerializer

    def get(self, request, *args, **kwargs):
        messages = TelegramMessage.objects.filter(user=request.user)
        serializer = TelegramMessageSerializer(messages, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class MessageSendAPIView(CreateAPIView):
    serializer_class = TelegramMessageSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.validated_data["user"] = request.user
        TelegramService.send_message_to_user(
            user=request.user, message=serializer.validated_data["message"]
        )
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
