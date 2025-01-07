# eos/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.student_list, name='student_list'),
    path('analysis/', views.run_analysis, name='run_analysis'),
    path('create/', views.create_student, name='create_student'),
    path('edit/<int:student_id>/', views.edit_student, name='edit_student'),
    path('view/<int:student_id>/', views.view_student, name='view_student'),
]
