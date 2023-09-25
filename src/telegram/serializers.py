from rest_framework import serializers

from telegram.models import TelegramMessage


class TelegramMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = TelegramMessage

        fields = ("id", "user", "date_sent", "message")

        read_only_fields = ("user",)
