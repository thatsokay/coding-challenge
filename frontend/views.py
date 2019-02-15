import json
from django.shortcuts import render
from django_celery_results.models import TaskResult


def index(request):
    query = TaskResult.objects.order_by('-date_done')
    context = {'jobs': json.dumps([
        {'url': task.task_args[2:-2], 'result': task.result}
        for task in query
    ])}
    return render(request, 'frontend/index.html', context)
