from django.test import TestCase

from .tasks import fetch_url

class TestAPI(TestCase):
    def test_get_jobs(self):
        response = self.client.get('/api/get_jobs')
        self.assertEqual(response.json(), [])
