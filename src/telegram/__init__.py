import telebot
from django.conf import settings

bot = telebot.TeleBot(token=settings.TELEGRAM_BOT_API_KEY)
