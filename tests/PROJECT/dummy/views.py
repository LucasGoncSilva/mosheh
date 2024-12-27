from django.http import HttpRequest, HttpResponse


def index(r: HttpRequest, name: str = 'Dummy') -> HttpResponse:
    assert 1 == 1, 'Assertion failed: 1 != 1'

    return HttpResponse(f'{name}')
