from pathlib import Path
from typing import Final

from django.contrib.messages import constants as messages


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY: str = 'cw%t5oij*-s6g8xmgkp6__4br))7&01!3+6_r7vw0p6y37aztqvc_@_tz+oo!ga9&-=2_%!qx+k(0e=y)!i_e=s+5vlzonba^m3)'  # noqa: E501


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG: bool = True
ALLOWED_HOSTS: list[str] = ['*', 'localhost']
SESSION_COOKIE_SECURE: bool = True
CSRF_COOKIE_SECURE: bool = True


# Application definition
INSTALLED_APPS: list[str] = [
    # Default
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # 3rd party
    'whitenoise',
    'captcha',
    'csp',
    # Local
    'account',
    'home',
    'secret',
    'err',
    'mail',
    'general',
    'plans',
]

MIDDLEWARE: list[str] = [
    'django.middleware.security.SecurityMiddleware',
    'csp.middleware.CSPMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF: Final[str] = 'CORE.urls'

TEMPLATES: Final[list[dict[str, str | list[Path] | bool | dict[str, list[str]]]]] = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION: Final[str] = 'CORE.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES: dict[str, dict[str, str | Path]] = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS: list[dict[str, str]] = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',  # noqa: E501
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE: Final[str] = 'en'

TIME_ZONE: Final[str] = 'America/Sao_Paulo'

USE_I18N: Final[bool] = True

USE_TZ: Final[bool] = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL: Final[str] = '/static/'
STATIC_ROOT: Final[Path] = BASE_DIR / 'staticfiles'
STATICFILES_DIRS: Final[list[Path]] = [
    BASE_DIR / 'static',
]
STATICFILES_STORAGE: Final[str] = (
    'whitenoise.storage.CompressedManifestStaticFilesStorage'
)


# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD: Final[str] = 'django.db.models.BigAutoField'


# User Model
AUTH_USER_MODEL: Final[str] = 'account.User'
LOGOUT_REDIRECT_URL: Final[str] = 'account/login'


# Argon2 Hash Algo
PASSWORD_HASHERS: list[str] = [
    'django.contrib.auth.hashers.Argon2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
    'django.contrib.auth.hashers.BCryptSHA256PasswordHasher',
    'django.contrib.auth.hashers.ScryptPasswordHasher',
]


# Messages configs
MESSAGE_TAGS: dict[int, str] = {
    messages.DEBUG: 'alert-debug',
    messages.INFO: 'alert-info',
    messages.SUCCESS: 'alert-success',
    messages.WARNING: 'alert-warning',
    messages.ERROR: 'alert-error',
}
