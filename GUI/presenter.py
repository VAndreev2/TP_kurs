import tkinter as tk
from tkinter import ttk, messagebox
from database import get_all_students, get_student_grades, add_student, update_student, add_student_grade, delete_student_grade
from analytics import AnalyticsEngine, PerformanceAnalytics, MajorAnalytics, YearAttendanceAnalytics

class Presenter:

    def __init__(self, root, view):
        self.root = root
        self.view = view
        self.notebook = view.notebook
        self.students_frame = view.students_frame
        self.edit_student_frame = view.edit_student_frame

        self.current_student_id = None

        self.analytics_engine = AnalyticsEngine()
        self.analytics_engine.register_module(PerformanceAnalytics())
        self.analytics_engine.register_module(MajorAnalytics())
        self.analytics_engine.register_module(YearAttendanceAnalytics())

    def load_students(self):
        for row in self.view.tree.get_children():
            self.view.tree.delete(row)
        students = get_all_students()
        for student in students:
            self.view.tree.insert("", "end", values=(student[0], student[1], student[2], student[4], student[5], "Изменить"), tags=(student[0],))

    def search_student(self):
        query = self.view.search_entry.get()
        if query:
            if query.isdigit():
                students = [student for student in get_all_students() if student[0] == int(query)]
            else:
                students = [student for student in get_all_students() if query.lower() in student[1].lower()]
        else:
            students = get_all_students()
        for row in self.view.tree.get_children():
            self.view.tree.delete(row)
        for student in students:
            self.view.tree.insert("", "end", values=(student[0], student[1], student[2], student[4], student[5], "Изменить"), tags=(student[0],))

    def on_tree_select(self, event):
        selected_item = self.view.tree.selection()
        if selected_item:
            item = self.view.tree.item(selected_item)
            student_id = item['values'][0]
            self.current_student_id = student_id
            self.open_edit_student(student_id)

    def open_create_student(self):
        self.notebook.tab(1, state='normal')
        self.notebook.select(self.edit_student_frame)
        self.create_edit_student_widgets(is_new=True)

    def open_edit_student(self, student_id):
        self.notebook.tab(1, state='normal')
        self.notebook.select(self.edit_student_frame)
        self.create_edit_student_widgets(student_id=student_id, is_new=False)

    def create_edit_student_widgets(self, student_id=None, is_new=False):
        for widget in self.edit_student_frame.winfo_children():
            widget.destroy()

        if not is_new:
            students = [student for student in get_all_students() if student[0] == student_id]
            if students:
                student = students[0]
                grades = get_student_grades(student_id)
            else:
                messagebox.showerror("Ошибка", "Студент не найден!")
                self.notebook.select(self.students_frame)
                return
        else:
            student = [None, "", 0, "", "", 0, 0]
            grades = []

        self.view.name_label = tk.Label(self.edit_student_frame, text="Имя")
        self.view.name_label.pack()
        self.view.name_entry = tk.Entry(self.edit_student_frame)
        self.view.name_entry.insert(0, student[1] if student[1] else "")
        self.view.name_entry.pack()

        self.view.age_label = tk.Label(self.edit_student_frame, text="Возраст")
        self.view.age_label.pack()
        self.view.age_entry = tk.Entry(self.edit_student_frame)
        self.view.age_entry.insert(0, student[2] if student[2] else "")
        self.view.age_entry.pack()

        self.view.email_label = tk.Label(self.edit_student_frame, text="Email")
        self.view.email_label.pack()
        self.view.email_entry = tk.Entry(self.edit_student_frame)
        self.view.email_entry.insert(0, student[3] if student[3] else "")
        self.view.email_entry.pack()

        self.view.major_label = tk.Label(self.edit_student_frame, text="Специальность")
        self.view.major_label.pack()
        self.view.major_entry = tk.Entry(self.edit_student_frame)
        self.view.major_entry.insert(0, student[4] if student[4] else "")
        self.view.major_entry.pack()

        self.view.year_label = tk.Label(self.edit_student_frame, text="Курс")
        self.view.year_label.pack()
        self.view.year_entry = tk.Entry(self.edit_student_frame)
        self.view.year_entry.insert(0, student[5] if student[5] else "")
        self.view.year_entry.pack()

        self.view.missed_hours_label = tk.Label(self.edit_student_frame, text="Пропущенные часы")
        self.view.missed_hours_label.pack()
        self.view.missed_hours_entry = tk.Entry(self.edit_student_frame)
        self.view.missed_hours_entry.insert(0, student[6] if student[6] else "")
        self.view.missed_hours_entry.pack()

        self.view.grades_label = tk.Label(self.edit_student_frame, text="Успеваемость")
        self.view.grades_label.pack()

        self.view.grades_frame = tk.Frame(self.edit_student_frame)
        self.view.grades_frame.pack()

        self.view.subject_label = tk.Label(self.view.grades_frame, text="Дисциплина")
        self.view.subject_label.grid(row=0, column=0, padx=5, pady=5)
        self.view.score_label = tk.Label(self.view.grades_frame, text="Баллы")
        self.view.score_label.grid(row=0, column=1, padx=5, pady=5)
        self.view.delete_label = tk.Label(self.view.grades_frame, text="Удалить")
        self.view.delete_label.grid(row=0, column=2, padx=5, pady=5)

        self.view.grades_entries = []
        for i, grade in enumerate(grades):
            subject_entry = tk.Entry(self.view.grades_frame)
            subject_entry.insert(0, grade['subject'] if grade['subject'] else "")
            subject_entry.grid(row=i+1, column=0, padx=5, pady=5)
            score_entry = tk.Entry(self.view.grades_frame)
            score_entry.insert(0, str(grade['score']) if grade['score'] else "")
            score_entry.grid(row=i+1, column=1, padx=5, pady=5)
            delete_button = tk.Button(self.view.grades_frame, text="Удалить", command=lambda gid=grade['id']: self.delete_grade(gid))
            delete_button.grid(row=i+1, column=2, padx=5, pady=5)
            self.view.grades_entries.append((subject_entry, score_entry, delete_button))

        self.view.add_grade_button = tk.Button(self.edit_student_frame, text="Добавить дисциплину", command=self.add_grade_row)
        self.view.add_grade_button.pack(pady=5)

        self.view.save_button = tk.Button(self.edit_student_frame, text="Сохранить", command=lambda: self.save_student(student_id if not is_new else None))
        self.view.save_button.pack(pady=5)

        self.view.cancel_button = tk.Button(self.edit_student_frame, text="Отмена", command=self.cancel_edit)
        self.view.cancel_button.pack(pady=5)

        self.view.view_student_button = tk.Button(self.edit_student_frame, text="Просмотр студента", command=lambda: self.open_view_student(student_id))
        self.view.view_student_button.pack(pady=5)

        if is_new:
            self.view.view_student_button.config(state='disabled')
        else:
            self.view.view_student_button.config(state='normal')

    def add_grade_row(self):
        subject_entry = tk.Entry(self.view.grades_frame)
        subject_entry.grid(row=len(self.view.grades_entries)+1, column=0, padx=5, pady=5)
        score_entry = tk.Entry(self.view.grades_frame)
        score_entry.grid(row=len(self.view.grades_entries)+1, column=1, padx=5, pady=5)
        delete_button = tk.Button(self.view.grades_frame, text="Удалить", command=lambda: messagebox.showinfo("Информация", "Нельзя удалить несохраненную оценку"))
        delete_button.grid(row=len(self.view.grades_entries)+1, column=2, padx=5, pady=5)
        self.view.grades_entries.append((subject_entry, score_entry, delete_button))

    def delete_grade(self, grade_id):
        delete_student_grade(grade_id)
        self.load_students()
        if self.current_student_id:
            self.open_edit_student(self.current_student_id)

    def save_student(self, student_id):
        name = self.view.name_entry.get()
        age = self.view.age_entry.get()
        email = self.view.email_entry.get()
        major = self.view.major_entry.get()
        year = self.view.year_entry.get()
        missed_hours = self.view.missed_hours_entry.get()

        if name and age and major and year and missed_hours:
            if student_id is None:
                add_student(name, age, email, major, year, missed_hours)
                student_id = get_all_students()[-1][0]
            else:
                update_student(student_id, name, age, email, major, year, missed_hours)

            for subject_entry, score_entry, _ in self.view.grades_entries:
                subject = subject_entry.get()
                score = score_entry.get()
                if subject and score:
                    add_student_grade(student_id, subject, score)

            self.load_students()
            messagebox.showinfo("Успех", "Студент сохранен успешно!")
            self.notebook.select(self.students_frame)
        else:
            messagebox.showerror("Ошибка", "Все поля должны быть заполнены!")

    def cancel_edit(self):
        self.notebook.tab(1, state='hidden')
        self.notebook.select(self.students_frame)

    def open_view_student(self, student_id):
        view_window = tk.Toplevel(self.root)
        view_window.title("Просмотр студента")
        view_window.geometry("400x400")
        self.create_view_student_widgets(view_window, student_id=student_id)

    def create_view_student_widgets(self, parent, student_id=None):
        for widget in parent.winfo_children():
            widget.destroy()

        if student_id:
            students = [student for student in get_all_students() if student[0] == student_id]
            if students:
                student = students[0]
                grades = get_student_grades(student_id)
            else:
                messagebox.showerror("Ошибка", "Студент не найден!")
                parent.destroy()
                return
        else:
            student = [None, "", 0, "", "", 0, 0]
            grades = []

        self.view.name_label = tk.Label(parent, text="Имя")
        self.view.name_label.pack()
        self.view.name_entry = tk.Label(parent, text=student[1] if student[1] else "")
        self.view.name_entry.pack()

        self.view.age_label = tk.Label(parent, text="Возраст")
        self.view.age_label.pack()
        self.view.age_entry = tk.Label(parent, text=student[2] if student[2] else "")
        self.view.age_entry.pack()

        self.view.email_label = tk.Label(parent, text="Email")
        self.view.email_label.pack()
        self.view.email_entry = tk.Label(parent, text=student[3] if student[3] else "")
        self.view.email_entry.pack()

        self.view.major_label = tk.Label(parent, text="Специальность")
        self.view.major_label.pack()
        self.view.major_entry = tk.Label(parent, text=student[4] if student[4] else "")
        self.view.major_entry.pack()

        self.view.year_label = tk.Label(parent, text="Курс")
        self.view.year_label.pack()
        self.view.year_entry = tk.Label(parent, text=student[5] if student[5] else "")
        self.view.year_entry.pack()

        self.view.missed_hours_label = tk.Label(parent, text="Пропущенные часы")
        self.view.missed_hours_label.pack()
        self.view.missed_hours_entry = tk.Label(parent, text=student[6] if student[6] else "")
        self.view.missed_hours_entry.pack()

        self.view.grades_label = tk.Label(parent, text="Успеваемость")
        self.view.grades_label.pack()

        self.view.grades_frame = tk.Frame(parent)
        self.view.grades_frame.pack()

        self.view.subject_label = tk.Label(self.view.grades_frame, text="Дисциплина")
        self.view.subject_label.grid(row=0, column=0, padx=5, pady=5)
        self.view.score_label = tk.Label(self.view.grades_frame, text="Баллы")
        self.view.score_label.grid(row=0, column=1, padx=5, pady=5)

        for i, grade in enumerate(grades):
            subject_entry = tk.Label(self.view.grades_frame, text=grade['subject'] if grade['subject'] else "")
            subject_entry.grid(row=i+1, column=0, padx=5, pady=5)
            score_entry = tk.Label(self.view.grades_frame, text=str(grade['score']) if grade['score'] else "")
            score_entry.grid(row=i+1, column=1, padx=5, pady=5)

        self.view.back_button = tk.Button(parent, text="Назад", command=parent.destroy)
        self.view.back_button.pack(pady=5)

    def on_tab_changed(self, event):
        if self.notebook.select() == '.!notebook.!frame2':
            return
        self.notebook.tab(1, state='hidden')

    def run_analysis(self):
        analysis_window = tk.Toplevel(self.root)
        analysis_window.title("Анализ данных")
        analysis_window.geometry("1050x780")

        analysis_window.protocol("WM_DELETE_WINDOW", lambda: analysis_window.destroy())

        students = get_all_students()
        student_data = [
            {
                "id": student[0],
                "name": student[1],
                "age": student[2],
                "grades": get_student_grades(student[0]),
                "email": student[3],
                "major": student[4],
                "year": student[5],
                "missed_hours": student[6]
            }
            for student in students
        ]

        analysis_results = self.analytics_engine.run_analysis(student_data, "missed_hours")

        self.create_analysis_widgets(analysis_window, analysis_results)

    def create_analysis_widgets(self, parent, analysis_results):
        for widget in parent.winfo_children():
            widget.destroy()

        canvas = tk.Canvas(parent)
        scrollbar = tk.Scrollbar(parent, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        for module, result in analysis_results.items():
            if module != 'statistics':
                frame = tk.Frame(scrollable_frame)
                frame.pack(pady=10)

                label = tk.Label(frame, text=result['name'], font=(20))
                label.pack()

                img_data = result['plot']
                img = tk.PhotoImage(data=img_data)
                img_label = tk.Label(frame, image=img)
                img_label.image = img
                img_label.pack()

        stats_frame = tk.Frame(scrollable_frame)
        stats_frame.pack(pady=10)

        stats_label = tk.Label(stats_frame, text="Статистика")
        stats_label.pack()

        tree = ttk.Treeview(stats_frame, columns=("Метр", "Значение"), show="headings", height=5)
        tree.heading("Метр", text="Метрика")
        tree.heading("Значение", text="Значение")
        tree.column("Метр", anchor=tk.W, width=300)
        tree.column("Значение", anchor=tk.CENTER, width=150)
        stats = analysis_results['statistics']
        for stat, value in stats.items():
            tree.insert("", tk.END, values=(stat, value))

        tree.pack()

        back_button = tk.Button(scrollable_frame, text="Назад", command=parent.destroy)
        back_button.pack(pady=5)

