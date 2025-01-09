# eos/tests.py

from django.test import TestCase, Client
from django.urls import reverse
from eos.models import Student, StudentGrade
from eos.forms import StudentForm, StudentEditForm, StudentGradeForm, StudentGradeFormSet
from eos.analytics import AnalyticsEngine, PerformanceAnalytics, MajorAnalytics, YearAttendanceAnalytics, \
    BarPlotStrategy
from eos.analytics_service import AnalyticsService


class StudentViewsTest(TestCase):

    def test_student_list_view(self):
        response = self.client.get(reverse('student_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'eos/index.html')

    def test_student_list_view_with_query(self):
        response = self.client.get(reverse('student_list'), {'q': 'John'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'eos/index.html')

    def test_create_student_view_get(self):
        response = self.client.get(reverse('create_student'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'eos/create_student.html')

    def test_register_module(self):
        module = PerformanceAnalytics(
            plot_strategy=BarPlotStrategy(xlabel='Subject', ylabel='Average Score', title='Average Scores'))
        engine = AnalyticsEngine()
        engine.register_module(module)
        self.assertIn(module, engine.modules)

    def test_analyze_grades(self):
        self.grades_data = [
            {
                "grades": [{"subject": "Math", "score": 85}, {"subject": "Science", "score": 90}]
            },
            {
                "grades": [{"subject": "Math", "score": 90}, {"subject": "Science", "score": 100}]
            },
        ]
        analytics = PerformanceAnalytics(plot_strategy=BarPlotStrategy(xlabel='Дисциплина', ylabel='Средний балл',
                                                                       title='Средний балл по дисциплинам'))
        result = analytics.analyze(self.grades_data)
        expected_result = {'Math': 87.5, 'Science': 95.0}
        self.assertEqual(result, expected_result)

    def test_analyze_major(self):
        self.major_data = [
            {
                "major": "Computer Science"
            },
            {
                "major": "Mathematics"
            },
        ]
        analytics = MajorAnalytics(plot_strategy=BarPlotStrategy(xlabel="Направления", ylabel="Количество студентов", title="Распределение студентов по направлениям"))
        result = analytics.analyze(self.major_data)
        expected_result = {'Computer Science': 1, 'Mathematics': 1}
        self.assertEqual(result, expected_result)

    def test_analyze_missed_hours(self):
        self.missed_data = [
            {
                "year": 2,
                "missed_hours": 10,
            },
            {
                "year": 2,
                "missed_hours": 90,
            },
        ]
        analytics = YearAttendanceAnalytics(plot_strategy=BarPlotStrategy(xlabel="Направления", ylabel="Количество студентов", title="Распределение студентов по направлениям"))
        result = analytics.analyze(self.missed_data)
        expected_result = {2: 50}
        self.assertEqual(result, expected_result)

    def test_analyze_service(self):
        data = [
            {"id": 1, "missed_hours": 5},
            {"id": 2, "missed_hours": 10},
            {"id": 3, "missed_hours": 15}
        ]
        service = AnalyticsService(data)
        statistics = service.calculate_statistics('missed_hours')
        expected_statistics = {
            'sum': 30,
            'mean': 10.0,
            'median': 10.0,
            'max': 15,
            'min': 5
        }
        self.assertEqual(statistics, expected_statistics)
