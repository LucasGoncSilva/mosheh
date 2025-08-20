from typing import Final

from django.db.models import DateField, Model


class WakeDatabase(Model):
    created: Final[DateField] = DateField(auto_created=True, auto_now_add=True)
