from typing import Final

from django.urls import URLPattern, path

from dummy.views import index


app_name: Final[str] = 'dummy'

urlpatterns: list[URLPattern] = [path('', index, name='index')]
