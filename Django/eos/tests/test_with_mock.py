# tests.py

from unittest.mock import patch
from django.test import TestCase, Client
from django.urls import reverse
from eos.models import Student

class MockAnalyticsService:
    def calculate_statistics(self, column_name):
        return {
            "sum": 100,
            "mean": 25,
            "median": 30,
            "max": 50,
            "min": 10,
        }

class StudentViewsTestWithMock(TestCase):

    @patch('eos.analytics.AnalyticsEngine.run_analysis', return_value={'statistics': MockAnalyticsService().calculate_statistics('missed_hours')})
    def test_run_analysis_view(self, mock_run_analysis):
        response = self.client.get(reverse('run_analysis'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'eos/analysis_results.html')
        self.assertContains(response, 'Среднее количество пропущенных часов')
        self.assertContains(response, '25')
