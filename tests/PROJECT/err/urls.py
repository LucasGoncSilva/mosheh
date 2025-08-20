from typing import Final

from django.urls import URLPattern, path

from err.views import handle403, handle404, handle500


app_name: Final[str] = 'err'

urlpatterns: list[URLPattern] = [
    path('403', handle403, name='403'),
    path('404', handle404, name='404'),
    path('500', handle500, name='500'),
]
