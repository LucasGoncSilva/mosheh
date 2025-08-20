from datetime import datetime
from os import getenv
from typing import Any, Final, Self
from uuid import uuid4

from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.core.validators import MaxLengthValidator, MinLengthValidator
from django.db.models import (
    CASCADE,
    BooleanField,
    CharField,
    DateTimeField,
    ForeignKey,
    Model,
    UUIDField,
)


class sWardenUserManager(BaseUserManager):
    def create_user(
        self: Self, username: str, password: str | None = None, **extra_fields: Any
    ) -> Self:
        if not username:
            raise ValueError('Username is required.')

        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(
        self: Self, username: str, password: str | None = None, **extra_fields
    ) -> Self:
        if getenv('DJANGO_SETTINGS_MODULE', 'CORE.settings.dev') == 'CORE.settings.dev':
            extra_fields.setdefault('is_staff', True)
            extra_fields.setdefault('is_superuser', True)
            extra_fields.setdefault('is_active', True)
            return self.create_user(username, password, **extra_fields)

        raise PermissionError('This environ cannot proceed with this operation.')


class User(AbstractBaseUser, PermissionsMixin):
    id: Final[UUIDField] = UUIDField(
        default=uuid4, unique=True, primary_key=True, editable=False
    )
    username: Final[CharField] = CharField(max_length=20, unique=True)
    is_staff: Final[BooleanField] = BooleanField(default=False)
    is_active: BooleanField | bool = BooleanField(default=False)
    created: Final[DateTimeField] = DateTimeField(auto_now_add=True)

    USERNAME_FIELD: Final[str] = 'username'

    objects: sWardenUserManager = sWardenUserManager()  # type:ignore

    def __str__(self: Self) -> str:
        return self.username


class ActivationAccountToken(Model):
    id: Final[UUIDField] = UUIDField(
        default=uuid4, unique=True, primary_key=True, editable=False
    )
    user: Final[ForeignKey] = ForeignKey(User, on_delete=CASCADE)
    value: Final[CharField] = CharField(
        max_length=64, validators=[MinLengthValidator(64), MaxLengthValidator(64)]
    )
    used: BooleanField = BooleanField(default=False)
    created: Final[DateTimeField] = DateTimeField(auto_now_add=True)

    def __str__(self: Self) -> str:
        return f'{self.value}'

    def is_valid(self: Self) -> bool:
        if (
            self.value
            and len(self.value) == 64
            and isinstance(self.used, bool)
            and self.created
            and isinstance(self.created, datetime)
        ):
            return True
        return False
