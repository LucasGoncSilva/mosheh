from os import getenv
from typing import Final

from debug_toolbar.toolbar import debug_toolbar_urls
from django.contrib import admin
from django.contrib.auth.views import (
    PasswordResetCompleteView,
    PasswordResetConfirmView,
    PasswordResetDoneView,
    PasswordResetView,
)
from django.urls import URLPattern, URLResolver, include, path


urlpatterns: list[URLResolver | URLPattern] = [
    # System functionality's pages
    path(
        'reset',
        PasswordResetView.as_view(template_name='account/password_reset.html'),
        name='password_reset',
    ),
    path(
        'reset-sent',
        PasswordResetDoneView.as_view(template_name='account/password_reset_done.html'),
        name='password_reset_done',
    ),
    path(
        'reset/<uidb64>/<token>',
        PasswordResetConfirmView.as_view(
            template_name='account/password_reset_confirm.html'
        ),
        name='password_reset_confirm',
    ),
    path(
        'reset-complete',
        PasswordResetCompleteView.as_view(
            template_name='account/password_reset_complete.html'
        ),
        name='password_reset_complete',
    ),
    path('captcha/', include('captcha.urls')),
    path('send-email/', include('mail.urls')),
    path('error/', include('err.urls')),
    # User's pages
    path('', include('home.urls')),
    path('account/', include('account.urls')),
    path('secrets/', include('secret.urls')),
    path('general/', include('general.urls')),
    path('plans/', include('plans.urls')),
]

if getenv('DJANGO_SETTINGS_MODULE', 'CORE.settings.dev') == 'CORE.settings.dev':
    urlpatterns += [
        path(f'{getenv("ADMIN", "__manager__")}/', admin.site.urls)
    ] + debug_toolbar_urls()

handler403: Final[str] = 'err.views.handle403'
handler404: Final[str] = 'err.views.handle404'
handler500: Final[str] = 'err.views.handle500'
