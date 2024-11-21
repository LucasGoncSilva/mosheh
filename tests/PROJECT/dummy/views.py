from django.http import HttpRequest, HttpResponse


def index(r: HttpRequest, name: str = 'Dummy') -> HttpResponse:
    return HttpResponse(f'{r.path} + {name}')
