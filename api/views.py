from django.http import HttpResponse
from .tasks import fetch_url

def add_job(request):
    fetch_url.delay()
    return HttpResponse(status=200)
