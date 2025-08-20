from django.urls import URLPattern, path

from plans.views import index


app_name: str = 'plans'

urlpatterns: list[URLPattern] = [path('', index, name='index')]
