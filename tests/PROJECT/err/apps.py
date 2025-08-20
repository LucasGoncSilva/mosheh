from typing import Final

from django.apps import AppConfig


class ErrConfig(AppConfig):
    default_auto_field: Final[str] = 'django.db.models.BigAutoField'
    name: str = 'err'
