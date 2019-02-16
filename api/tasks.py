import requests
from celery import shared_task

@shared_task
def fetch_url(url):
    for i in range(3):
        try:
            response = requests.get(url)
            if response.ok:
                break
        except (requests.RequestException, requests.ConnectionError) as e:
            return str(e)
    return response.status_code
