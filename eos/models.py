# eos/models.py

from django.db import models

class Student(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    email = models.EmailField(blank=True, null=True)
    major = models.CharField(max_length=100)
    year = models.IntegerField()
    missed_hours = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.name} ({self.student_id})"

class StudentGrade(models.Model):
    student = models.ForeignKey(Student, related_name='grades', on_delete=models.CASCADE)
    subject = models.CharField(max_length=100)
    score = models.FloatField()

    def __str__(self):
        return f"{self.subject}: {self.score}"
