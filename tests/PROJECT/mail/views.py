from django.db.models import QuerySet
from django.http import HttpRequest, HttpResponse

from mail.models import WakeDatabase


def wake_db(r: HttpRequest) -> HttpResponse:
    WakeDatabase.objects.create()

    e: QuerySet = WakeDatabase.objects.all()

    if e.count() > 3:
        e.delete()

    return HttpResponse(e.count())
