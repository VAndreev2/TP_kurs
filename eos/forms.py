# eos/forms.py

from django import forms
from .models import Student, StudentGrade

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['name', 'age', 'major', 'year']

        labels = {
            'name': 'Имя',
            'age': 'Возраст',
            'major': 'Специальность',
            'year': 'Курс',
        }

class StudentEditForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['name', 'age', 'email', 'major', 'year', 'missed_hours']

        labels = {
            'name': 'Имя',
            'age': 'Возраст',
            'email': 'Email',
            'major': 'Специальность',
            'year': 'Курс',
            'missed_hours': 'Пропущенные часы',
        }

class StudentGradeForm(forms.ModelForm):
    class Meta:
        model = StudentGrade
        fields = ['subject', 'score']

StudentGradeFormSet = forms.inlineformset_factory(
    Student, StudentGrade, form=StudentGradeForm, extra=1, can_delete=True
)
