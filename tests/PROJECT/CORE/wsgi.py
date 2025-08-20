import os

from django.core.wsgi import get_wsgi_application


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'CORE.settings.dev')

app = application = get_wsgi_application()
