from telebot import types

from telegram import bot
from users.models import User
from users.services import FernetService


@bot.message_handler(commands=["start"])
def start_handler(message: types.Message):
    user_id = message.from_user.id
    username = message.from_user.username
    bot.send_message(
        user_id,
        text=f"Привет {username}! \nЯ ваш Telegram бот который будет дублировать ваши сообщения."
        "\nДля того чтобы ваши сообщения дублировались здесь:"
        "\n1. Сначала зарегистрируйтесь на сайте."
        "\n2. Сгенерируйте токен в личном профиле."
        "\n3. Скопируйте токен и отправьте мне.",
    )


@bot.message_handler(func=lambda message: True)
def handle_token(message: types.Message) -> None:
    token = message.text
    if not token:
        bot.reply_to(message, "Пожалуйста, введите ваш токен.")

    username = FernetService.decode_token(token=token)
    if username is None:
        bot.reply_to(message, "Пожалуйста, введите правильный токен.")

    else:
        existing_user = User.objects.get(username=username)
        existing_user.telegram_id = message.from_user.id
        existing_user.telegram_username = message.from_user.username
        existing_user.save()
        bot.reply_to(message, "Токен подтвержден, дублирование сообщений активирована")
