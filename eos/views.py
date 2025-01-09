# views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.forms import inlineformset_factory
from .models import Student, StudentGrade
from .forms import StudentForm, StudentEditForm, StudentGradeForm, StudentGradeFormSet
from .analytics import AnalyticsEngine, PerformanceAnalytics, MajorAnalytics, YearAttendanceAnalytics, BarPlotStrategy, LinePlotStrategy
from .analytics_service import AnalyticsService

def student_list(request):
    query = request.GET.get('q')
    if query:
        if query.isdigit():
            students = Student.objects.filter(id=query)
        else:
            students = Student.objects.filter(name__icontains=query)
    else:
        students = Student.objects.all()
    return render(request, 'eos/index.html', {'students': students})

def run_analysis(request):
    students = Student.objects.all()
    engine = AnalyticsEngine()
    engine.register_module(PerformanceAnalytics(plot_strategy=BarPlotStrategy(
            xlabel='Дисциплина', ylabel='Средний балл', title='Средний балл по дисциплинам')))
    engine.register_module(MajorAnalytics(plot_strategy=BarPlotStrategy(
            xlabel="Направления", ylabel="Количество студентов", title="Распределение студентов по направлениям")))
    engine.register_module(YearAttendanceAnalytics(plot_strategy=BarPlotStrategy(
            xlabel='Курс обучения', ylabel='Пропущенные часы', title='Анализ посещаемости по годам обучения (среднее значение)')))

    analysis_results = engine.run_analysis(students, 'missed_hours')
    return render(request, 'eos/analysis_results.html', {'results': analysis_results})

def create_student(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('student_list')
    else:
        form = StudentForm()
    return render(request, 'eos/create_student.html', {'form': form})

def edit_student(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    if request.method == 'POST':
        form = StudentEditForm(request.POST, instance=student)
        formset = StudentGradeFormSet(request.POST, instance=student)
        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            return redirect('edit_student', student_id=student.id)
    else:
        form = StudentEditForm(instance=student)
        formset = StudentGradeFormSet(instance=student)
    return render(request, 'eos/edit_student.html', {'form': form, 'formset': formset, 'student_id': student_id})

def view_student(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    grades = student.grades.all()
    return render(request, 'eos/view_student.html', {'student': student, 'grades': grades, 'student_id': student_id})
