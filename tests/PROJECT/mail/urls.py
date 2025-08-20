from typing import Final

from django.urls import URLPattern, path

from mail.views import wake_db


app_name: Final[str] = 'mail'

urlpatterns: list[URLPattern] = [
    path('wake', wake_db, name='wake'),
]
