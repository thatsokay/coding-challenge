import json
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django_celery_results.models import TaskResult

from .tasks import fetch_url


@csrf_exempt
def add_job(request):
    if request.method != 'POST':
        return HttpResponse(status=405)

    try:
        data = json.loads(request.body)
        fetch_url.delay(data.get('url', ''))
    except json.JSONDecodeError:
        return HttpResponse(status=422)

    return HttpResponse(status=200)


def get_jobs(request):
    if request.method != 'GET':
        return HttpResponse(status=405)

    limit = int(request.GET.get('limit', '10'))
    offset = int(request.GET.get('offset', '0'))
    query = TaskResult.objects.order_by('-date_done')[offset:offset + limit]
    data = [{
        'time': task.date_done.strftime('%Y-%m-%d %H:%M'),
        'url': task.task_args[2:-2],
        'result': task.result,
    } for task in query]
    return JsonResponse(data, safe=False)
