import telebot

from telegram import bot
from users.models import User


class TelegramService:
    @classmethod
    def send_message_to_user(cls, user: User, message: str) -> None:
        users_telegram_id = user.telegram_id
        rendered_message = cls._rendered_message(
            user.telegram_username if user.telegram_username else user.username, message)

        try:
            bot.send_message(
                chat_id=users_telegram_id,
                text=rendered_message,
            )
        except telebot.apihelper.ApiTelegramException:
            raise Exception("Telegram sending error")

    @classmethod
    def _rendered_message(cls, username: str, message: str) -> str:
        return f"{username}, я получил от тебя сообщение:\n{message}"

