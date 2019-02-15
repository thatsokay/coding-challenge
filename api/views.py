from django.http import HttpResponse, JsonResponse
from django_celery_results.models import TaskResult

from .tasks import fetch_url

def add_job(request):
    fetch_url.delay('http://example.com')
    return HttpResponse(status=200)

def get_jobs(request):
    if request.method == 'GET':
        query = TaskResult.objects.order_by('-date_done')
        data = [{'url': task.task_args[2:-2], 'result': task.result} for task in query]
        return JsonResponse(data, safe=False)
    return HttpResponse(status=405)
