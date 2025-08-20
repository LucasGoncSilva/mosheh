from typing import Final

from django.urls import URLPattern, path

from general.views import index


app_name: Final[str] = 'general'

urlpatterns: list[URLPattern] = [
    path('', index, name='index'),
]
