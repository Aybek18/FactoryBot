import base64
from dataclasses import dataclass

from cryptography.fernet import Fernet
from django.conf import settings
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import AuthenticationFailed

from users.models import User


@dataclass
class FernetService:
    secret_key = settings.SECRET_KEY

    @classmethod
    def _fernet(cls) -> bytes:
        return base64.urlsafe_b64encode(cls.secret_key[:32].encode("utf-8"))

    @classmethod
    def generate_token(cls, username: str) -> bytes:
        """Простой алгоритм для генерации токена, куда передается секретный ключ и username пользователя"""
        cipher_suite = Fernet(cls._fernet())

        data_to_encrypt = f"{username}".encode('utf-8')

        token = cipher_suite.encrypt(data_to_encrypt)
        return token

    @classmethod
    def decode_token(cls, token) -> str:
        cipher_suite = Fernet(cls._fernet())
        try:
            decoded_data = cipher_suite.decrypt(token=token).decode("utf-8")
            return decoded_data
        except Exception as e:
            print(f"Ошибка при декодировании токена: {str(e)}")  # TODO можно добавить логирование вместо print()


class UserAuthService:
    @classmethod
    def create_user(cls, user_data: dict) -> str:
        user = User.objects.create_user(**user_data)
        return cls.user_token(user)

    @classmethod
    def login_user(cls, user_data: dict) -> str:
        user = authenticate(**user_data)
        if not user:
            raise AuthenticationFailed()
        return cls.user_token(user)

    @classmethod
    def user_token(cls, user: User) -> str:
        access_token, _ = Token.objects.get_or_create(user=user)
        return access_token.key
