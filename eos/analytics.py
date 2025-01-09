# analytics.py

from abc import ABC, abstractmethod
from typing import List, Dict, Type
from .models import Student, StudentGrade
import matplotlib.pyplot as plt
import io
import base64
from threading import Lock
from .analytics_service import AnalyticsService


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

    def __init__(self, plot_strategy: PlotStrategy):
        self.plot_strategy = plot_strategy

    @abstractmethod
    def analyze(self, data: List[Dict]) -> Dict:
        """Выполняет анализ данных."""
        pass

    def plot_graph(self, data: Dict) -> str:
        return self.plot_strategy.plot(data)


# Модуль аналитики успеваемости
class PerformanceAnalytics(AnalyticsModule):
    name = "Анализ успеваемости"

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

    def analyze(self, data: List[Dict]) -> Dict:
        """Выполняет анализ данных и возвращает средние пропущенные часы по годам."""
        year_attendance = {}
        for student_data in data:
            year = student_data['year']
            missed_hours = student_data['missed_hours']
            if year not in year_attendance:
                year_attendance[year] = []
            year_attendance[year].append(missed_hours)

        # Средние пропущенные часы по годам
        return {year: sum(hours) / len(hours) for year, hours in year_attendance.items()}


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

    def generate_student_data(self, students: List[Student]) -> List[Dict]:
        return [
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

    def calculate_statistics(self, data: List[Dict], column_name: str) -> Dict:
        analytics_service = AnalyticsService(data)
        return analytics_service.calculate_statistics(column_name)

    def analyze_modules(self, data: List[Dict]) -> Dict:
        results = {}
        for module in self.modules:
            module_result = module.analyze(data)
            results[module.name] = {
                'result': module_result,
                'plot': module.plot_graph(module_result),
                'name': module.name
            }
        return results
    def run_analysis(self, students: List[Student], column_name: str) -> Dict:
        # Генерация данных студентов
        data = self.generate_student_data(students)

        # Вычисление статистики
        statistics = self.calculate_statistics(data, column_name)

        # Анализ с использованием модулей
        module_results = self.analyze_modules(data)

        # Добавление статистики в результаты
        module_results['statistics'] = statistics

        return module_results
