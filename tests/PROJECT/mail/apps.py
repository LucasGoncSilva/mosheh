from typing import Final

from django.apps import AppConfig


class MailConfig(AppConfig):
    default_auto_field: Final[str] = 'django.db.models.BigAutoField'
    name: str = 'mail'
