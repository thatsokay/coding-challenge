from django.test import TestCase
from unittest import mock
from django_celery_results.models import TaskResult

from .tasks import fetch_url


class TestAPI(TestCase):
    def mocked_requests_get(*args, **kwargs):
        """
        Mock for testing with requests.
        """
        class MockResponse:
            def __init__(self, status_code):
                self.status_code = status_code

            def ok(self):
                return self.status_code < 400

        try:
            return MockResponse(int(args[0]))
        except ValueError:
            return MockResponse(404)


    @mock.patch('requests.get', side_effect=mocked_requests_get)
    def test_fetch_url(self, mock_get):
        """
        Test fetching external URLs.
        """
        self.assertEqual(fetch_url('200'), 200)
        self.assertEqual(fetch_url('400'), 400)


    def test_get_jobs(self):
        """
        Test getting job history.
        """
        TaskResult(task_id='test1', task_args="['test']", result='200').save()
        TaskResult(task_id='test2', task_args="['test']", result='400').save()
        response = self.client.get('/api/get_jobs')
        data = response.json()
        for job in data:
            del job['time']
        self.assertEqual(data, [
            {'url': 'test', 'result': '400'},
            {'url': 'test', 'result': '200'},
        ])
