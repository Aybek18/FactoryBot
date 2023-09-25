from django.db import models

from users.models import User


class TelegramMessage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_sent = models.DateTimeField(auto_now_add=True)
    message = models.TextField()
