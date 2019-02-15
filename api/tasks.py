from celery import shared_task

@shared_task
def fetch_url():
    return True
