from django.http import HttpRequest, HttpResponse


def index(r: HttpRequest) -> HttpResponse:
    return HttpResponse(r.path)
