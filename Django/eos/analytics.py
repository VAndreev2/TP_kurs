# analytics.py

from abc import ABC, abstractmethod
from typing import List, Dict, Type
from .models import Student, StudentGrade
import matplotlib.pyplot as plt
import io
import base64
from threading import Lock
from .analytics_service import AnalyticsService  # Импортируем новый сервис

# Базовый интерфейс для построения графиков
class PlotStrategy(ABC):
    @abstractmethod
    def plot(self, data: Dict) -> str:
        """Создаёт график и возвращает его в виде base64 строки."""
        pass

# Стратегия для построения столбчатых диаграмм
class BarPlotStrategy(PlotStrategy):
    def __init__(self, xlabel: str, ylabel: str, title: str):
        self.xlabel = xlabel
        self.ylabel = ylabel
        self.title = title

    def plot(self, data: Dict) -> str:
        plt.figure(figsize=(10, 5))
        plt.bar(data.keys(), data.values())
        plt.xlabel(self.xlabel)
        plt.ylabel(self.ylabel)
        plt.title(self.title)

        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        image_png = buf.getvalue()
        buf.close()

        return base64.b64encode(image_png).decode('utf-8')

# Базовый интерфейс для всех аналитических модулей
class AnalyticsModule(ABC):
    name = ""

    @abstractmethod
    def analyze(self, data: List[Dict]) -> Dict:
        """Выполняет анализ данных."""
        pass

    def __init__(self, plot_strategy: PlotStrategy):
        self.plot_strategy = plot_strategy

    def plot(self, data: Dict) -> str:
        return self.plot_strategy.plot(data)

# Модуль аналитики успеваемости
class PerformanceAnalytics(AnalyticsModule):
    name = "Анализ успеваемости"

    def __init__(self):
        super().__init__(BarPlotStrategy(
            xlabel='Дисциплина', ylabel='Средний балл', title='Средний балл по дисциплинам'))

    def analyze(self, data: List[Dict]) -> Dict:
        subject_averages = {}
        for student_data in data:
            for grade in student_data['grades']:
                subject = grade['subject']
                score = grade['score']
                if subject not in subject_averages:
                    subject_averages[subject] = []
                subject_averages[subject].append(score)

        return {subject: sum(scores) / len(scores) for subject, scores in subject_averages.items()}

# Модуль аналитики направлений
class MajorAnalytics(AnalyticsModule):
    name = "Анализ направлений"

    def __init__(self):
        super().__init__(BarPlotStrategy(
            xlabel='Направления', ylabel='Количество студентов', title='Распределение студентов по направлениям'))

    def analyze(self, data: List[Dict]) -> Dict:
        major_counts = {}
        for student_data in data:
            major = student_data['major']
            if major not in major_counts:
                major_counts[major] = 0
            major_counts[major] += 1
        return major_counts

# Модуль аналитики посещаемости по годам обучения
class YearAttendanceAnalytics(AnalyticsModule):
    name = "Анализ посещаемости"

    def __init__(self):
        self.plot_strategy = BarPlotStrategy(
            xlabel='Год', ylabel='Пропущенные часы', title='Анализ посещаемости по годам обучения (среднее значение)')

    def analyze(self, data: List[Dict]) -> Dict:
        """Анализ посещаемости студентов по годам обучения."""
        year_attendance = {}
        for student_data in data:
            year = student_data['year']
            missed_hours = student_data['missed_hours']
            if year not in year_attendance:
                year_attendance[year] = []
            year_attendance[year].append(missed_hours)

        return {year: {"total_missed_hours": sum(hours), "average_missed_hours": sum(hours) / len(hours)} for year, hours in year_attendance.items()}

    def plot(self, data: Dict) -> str:
        years = list(data.keys())
        total_missed_hours = [info['total_missed_hours'] for info in data.values()]
        average_missed_hours = [info['average_missed_hours'] for info in data.values()]

        # Используем стратегию для построения графика
        return self.plot_strategy.plot(dict(zip(years, average_missed_hours)))




# Улучшенная реализация Singleton для AnalyticsEngine
class AnalyticsEngine:
    _instance = None
    _lock = Lock()

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(AnalyticsEngine, cls).__new__(cls)
            cls._instance.modules = []
        return cls._instance

    def register_module(self, module: AnalyticsModule):
        self.modules.append(module)

    def run_analysis(self, students: List[Student], column_name: str) -> Dict:
        results = {}
        data = [
            {
                "id": student.id,
                "name": student.name,
                "age": student.age,
                "grades": list(student.grades.values('subject', 'score')),
                "email": student.email,
                "major": student.major,
                "year": student.year,
                "missed_hours": student.missed_hours
            }
            for student in students
        ]

        # Используем AnalyticsService для вычисления статистики
        analytics_service = AnalyticsService(data)
        statistics = analytics_service.calculate_statistics(column_name)

        for module in self.modules:
            module_result = module.analyze(data)
            results[module.name] = {
                'result': module_result,
                'plot': module.plot(module_result),
                'name': module.name
            }

        # Добавляем статистику в результаты
        results['statistics'] = statistics

        return results