from gc import collect, freeze, set_threshold
from random import seed

from django.conf import settings


def gc_config() -> None:
    set_threshold(1000, 1000, 1000)
    collect()
    freeze()


def seed_config() -> None:
    seed(settings.SECRET_KEY)


def set_all() -> None:
    seed_config()
    gc_config()
