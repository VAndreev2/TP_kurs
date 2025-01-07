import os

import psycopg2
from psycopg2 import sql
from dotenv import load_dotenv

load_dotenv(dotenv_path='data.env')

DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD")
def create_connection():
    conn = psycopg2.connect(
        dbname="django_db",
        user="postgres",
        password=DATABASE_PASSWORD,
        host="localhost",
        port="5432"
    )
    return conn

def create_tables():
    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS eos_student (
            id SERIAL PRIMARY KEY,
            name TEXT NOT NULL,
            age INTEGER NOT NULL,
            email TEXT,
            major TEXT NOT NULL,
            year INTEGER NOT NULL,
            missed_hours INTEGER DEFAULT 0
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS eos_studentgrade (
            id SERIAL PRIMARY KEY,
            subject TEXT NOT NULL,
            score REAL NOT NULL,
            student_id INTEGER REFERENCES eos_student(id)
        )
    ''')

    conn.commit()
    conn.close()

def add_student(name, age, email, major, year, missed_hours):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO eos_student (name, age, email, major, year, missed_hours)
        VALUES (%s, %s, %s, %s, %s, %s)
    ''', (name, age, email, major, year, missed_hours))
    conn.commit()
    conn.close()

def update_student(student_id, name, age, email, major, year, missed_hours):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE eos_student
        SET name = %s, age = %s, email = %s, major = %s, year = %s, missed_hours = %s
        WHERE id = %s
    ''', (name, age, email, major, year, missed_hours, student_id))
    conn.commit()
    conn.close()

def add_student_grade(student_id, subject, score):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO eos_studentgrade (subject, score, student_id)
        VALUES (%s, %s, %s)
    ''', (subject, score, student_id))
    conn.commit()
    conn.close()

def update_student_grades(student_id, subject, score):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO eos_studentgrade (subject, score, student_id)
        VALUES (%s, %s, %s)
        ON CONFLICT (student_id, subject)
        DO UPDATE SET score = EXCLUDED.score
    ''', (subject, score, student_id))
    conn.commit()
    conn.close()

def delete_student_grade(grade_id):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('''
        DELETE FROM eos_studentgrade WHERE id = %s
    ''', (grade_id,))
    conn.commit()
    conn.close()

def get_all_students():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM eos_student')
    students = cursor.fetchall()
    conn.close()
    return students

def get_student_grades(student_id):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM eos_studentgrade WHERE student_id = %s', (student_id,))
    grades = cursor.fetchall()
    conn.close()

    # Преобразуем данные в список словарей
    grades_list = []
    for grade in grades:
        grades_list.append({
            'id': grade[0],
            'subject': grade[1],
            'score': grade[2],
            'student_id': grade[3]
        })
    return grades_list