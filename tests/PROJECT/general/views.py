from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render


@login_required(login_url='/account/login')
def index(r: HttpRequest) -> HttpResponse:
    return render(r, 'general/index.html')
