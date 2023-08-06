from django.conf import settings
from django.urls import path
from django.http import HttpResponse


def my_view(request):
    html = "<html><body>Hello World</body></html>"
    return HttpResponse(html)


urlpatterns = []


if settings.ADD_HELLO_URL:
    urlpatterns += [path('hello/', my_view, name='hello'), ]
