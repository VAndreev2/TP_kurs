# eos/tests.py

from django.test import TestCase, Client
from django.urls import reverse
from eos.models import Student, StudentGrade
from eos.forms import StudentForm, StudentEditForm, StudentGradeForm, StudentGradeFormSet

class StudentViewsTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.student = Student.objects.create(
            name='John Doe',
            age=20,
            email='john.doe@example.com',
            major='Computer Science',
            year=2,
            missed_hours=5
        )
        self.grade = StudentGrade.objects.create(
            student=self.student,
            subject='Math',
            score=90.0
        )

    def test_student_list_view(self):
        response = self.client.get(reverse('student_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'eos/index.html')
        self.assertContains(response, 'John Doe')

    def test_student_list_view_with_query(self):
        response = self.client.get(reverse('student_list'), {'q': 'John'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'eos/index.html')
        self.assertContains(response, 'John Doe')

    def test_run_analysis_view(self):
        response = self.client.get(reverse('run_analysis'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'eos/analysis_results.html')

    def test_create_student_view_get(self):
        response = self.client.get(reverse('create_student'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'eos/create_student.html')
        self.assertIsInstance(response.context['form'], StudentForm)

    def test_create_student_view_post(self):
        response = self.client.post(reverse('create_student'), {
            'name': 'Jane Doe',
            'age': 22,
            'email': 'jane.doe@example.com',
            'major': 'Physics',
            'year': 2,
            'missed_hours': 3
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Student.objects.count(), 2)
        self.assertEqual(Student.objects.last().name, 'Jane Doe')

    def test_edit_student_view_get(self):
        response = self.client.get(reverse('edit_student', args=[self.student.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'eos/edit_student.html')
        self.assertIsInstance(response.context['form'], StudentEditForm)
        self.assertIsInstance(response.context['formset'], StudentGradeFormSet)

    def test_edit_student_view_post(self):
        response = self.client.post(reverse('edit_student', args=[self.student.id]), {
            'name': 'John Doe',
            'age': 21,
            'email': 'john.doe@example.com',
            'major': 'Computer Science',
            'year': 2,
            'missed_hours': 5,
            'grades-TOTAL_FORMS': 1,
            'grades-INITIAL_FORMS': 1,
            'grades-MIN_NUM_FORMS': 0,
            'grades-MAX_NUM_FORMS': 1000,
            'grades-0-id': self.grade.id,
            'grades-0-student': self.student.id,
            'grades-0-subject': 'Math',
            'grades-0-score': 95.0
        })
        self.assertEqual(response.status_code, 302)
        self.student.refresh_from_db()
        self.assertEqual(self.student.age, 21)
        self.assertEqual(self.student.grades.first().score, 95.0)

    def test_view_student_view(self):
        response = self.client.get(reverse('view_student', args=[self.student.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'eos/view_student.html')
        self.assertContains(response, 'John Doe')
        self.assertContains(response, 'Math')