import tkinter as tk
from tkinter import ttk
from presenter import Presenter
from database import create_tables

class StudentApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Студенты")

        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(expand=1, fill="both")

        self.students_frame = ttk.Frame(self.notebook)
        self.edit_student_frame = ttk.Frame(self.notebook)

        self.notebook.add(self.students_frame, text="Студенты")
        self.notebook.add(self.edit_student_frame, text="Редактировать студента")

        self.notebook.tab(1, state='hidden')

        self.presenter = Presenter(self.root, self)

        self.notebook.bind("<<NotebookTabChanged>>", self.presenter.on_tab_changed)

        self.search_label = tk.Label(self.students_frame, text="Введите имя или ID")
        self.search_label.pack(pady=5)

        self.search_entry = tk.Entry(self.students_frame)
        self.search_entry.pack(pady=5)

        self.search_button = tk.Button(self.students_frame, text="Поиск", command=self.presenter.search_student)
        self.search_button.pack(pady=5)

        self.table_frame = tk.Frame(self.students_frame)
        self.table_frame.pack(pady=10)

        self.tree = ttk.Treeview(self.table_frame, columns=("ID", "ФИО", "Возраст", "Специальность", "Курс", "Действие"), show='headings')
        self.tree.heading("ID", text="ID")
        self.tree.heading("ФИО", text="ФИО")
        self.tree.heading("Возраст", text="Возраст")
        self.tree.heading("Специальность", text="Специальность")
        self.tree.heading("Курс", text="Курс")
        self.tree.heading("Действие", text="Действие")
        self.tree.column("ID", width=50)
        self.tree.column("ФИО", width=150)
        self.tree.column("Возраст", width=70)
        self.tree.column("Специальность", width=150)
        self.tree.column("Курс", width=50)
        self.tree.column("Действие", width=100)
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.tree.bind("<ButtonRelease-1>", self.presenter.on_tree_select)

        self.add_button = tk.Button(self.students_frame, text="Создать студента", command=self.presenter.open_create_student)
        self.add_button.pack(pady=10)

        self.analytics_button = tk.Button(self.students_frame, text="Анализ данных", command=self.presenter.run_analysis)
        self.analytics_button.pack(pady=10)

        self.presenter.load_students()

        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def on_closing(self):
        # Закрытие главного окна
        self.root.quit()
        self.root.destroy()


if __name__ == "__main__":
    create_tables()
    root = tk.Tk()
    app = StudentApp(root)
    root.mainloop()
