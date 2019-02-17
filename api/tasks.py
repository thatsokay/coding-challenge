import requests
from celery import shared_task

@shared_task
def fetch_url(url):
    """
    Send a GET request to the given URL. Makes 3 attempts to receive a response
    status less than 400.
    """
    for i in range(3):
        try:
            response = requests.get(url)
            if response.ok:
                break
        except (requests.RequestException, requests.ConnectionError) as e:
            return str(e)
    return response.status_code
