# ruff: noqa: F403

from os import getenv

from csp.constants import NONE, SELF
from dj_database_url import DBConfig, config

from CORE.settings.base import *
from CORE.settings.gconfig import set_all


DATABASES: dict[str, DBConfig] = {
    'default': config(default=str(getenv('DATABASE_URL')))
}

DEBUG: bool = bool(getenv('DEBUG', False))
SECRET_KEY: str | None = getenv('SECRET_KEY')
ALLOWED_HOSTS: list[str] = list(
    map(lambda url: url.strip(), str(getenv('ALLOWED_HOSTS')).split(','))
)

# General Security
SECURE_CROSS_ORIGIN_OPENER_POLICY: str = 'same-origin'
SECURE_CROSS_ORIGIN_EMBEDDER_POLICY: str = 'require-corp'
SECURE_CROSS_ORIGIN_RESOURCE_POLICY: str = 'same-origin'
SESSION_COOKIE_HTTPONLY: bool = True
CSRF_COOKIE_HTTPONLY: bool = True
SECURE_PROXY_SSL_HEADER: tuple[str, str] = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_SSL_REDIRECT: bool = True
SECURE_HSTS_SECONDS: int = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS: bool = True
SECURE_HSTS_PRELOAD: bool = True
CSRF_COOKIE_SECURE: bool = True
SESSION_COOKIE_SECURE: bool = True
SECURE_BROWSER_XSS_FILTER: bool = True
SECURE_CONTENT_TYPE_NOSNIFF: bool = True
X_FRAME_OPTIONS: str = 'DENY'
SECURE_REFERRER_POLICY: str = 'strict-origin'

# django-csp
CONTENT_SECURITY_POLICY = {
    'DIRECTIVES': {
        'default-src': [NONE],
        'script-src': [SELF],
        'style-src': [SELF],
        'img-src': [SELF],
        'font-src': [SELF],
        'connect-src': [SELF],
        'frame-ancestor': [NONE],
        'base-uri': [NONE],
        'form-action': [SELF],
        'upgrade-insecure-requests': True,
    },
}

set_all()
