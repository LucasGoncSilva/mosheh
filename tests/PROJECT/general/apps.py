from typing import Final

from django.apps import AppConfig


class GeneralConfig(AppConfig):
    default_auto_field: Final[str] = 'django.db.models.BigAutoField'
    name: str = 'general'
