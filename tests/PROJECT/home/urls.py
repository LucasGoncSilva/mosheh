from typing import Final

from django.urls import URLPattern, path

from home.views import cookies, faq, index, privacy, security, terms


app_name: Final[str] = 'home'

urlpatterns: list[URLPattern] = [
    path('', index, name='index'),
    path('FAQ', faq, name='faq'),
    path('terms', terms, name='terms'),
    path('privacy', privacy, name='privacy'),
    path('cookies', cookies, name='cookies'),
    path('security', security, name='security'),
]
