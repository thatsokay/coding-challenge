import json
import pytz
from django.shortcuts import render
from django_celery_results.models import TaskResult


def index(request):
    """
    Returns the frontend displaying the last 10 jobs.
    """
    query = TaskResult.objects.order_by('-date_done')[:10]
    context = {'jobs': json.dumps([{
        'time': task.date_done.astimezone(pytz.timezone('Australia/Brisbane')).strftime('%Y-%m-%d %H:%M'),
        'url': task.task_args[2:-2],
        'result': task.result,
    } for task in query])}
    return render(request, 'frontend/index.html', context)
