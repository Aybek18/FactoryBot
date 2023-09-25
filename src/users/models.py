from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models


class UserManager(BaseUserManager):
    """Custom user manager for User model with an email as a username"""

    use_in_migrations = True

    def _create_user(self, username: str, password: str, **extra_fields):
        if not username:
            raise ValueError("The given value must be set")
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username: str, password: str, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(username, password, **extra_fields)

    def create_superuser(self, username: str, password: str, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(username, password, **extra_fields)


class User(AbstractUser):
    email = None
    username = models.CharField(max_length=40, unique=True)
    REQUIRED_FIELDS = []
    objects = UserManager()
    telegram_id = models.IntegerField(null=True, blank=True)
    telegram_username = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self) -> str:
        return self.username
