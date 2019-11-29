# 1) Создать базу данных студентов (ФИО, группа, оценки, куратор студента, факультет).
# Написать CRUD ко всем полям. Описать методы для вывода отличников по каждому факультету.
# Вывести всех студентов определенного куратора.

from flask import Flask, render_template, request, redirect, url_for
from models import models
from random import randint, choice
from mongoengine import *

connect('students')
app = Flask(__name__)


@app.route('/')
def index():
    students = models.Student.objects()
    return render_template('index.html', students=students)


@app.route('/insert', methods=['POST'])
def insert():
    if request.method == 'POST':
        group = models.Group(**{'group_name': f'{request.form.get("group_name")}'}).save()
        curator = models.Curator(**{'curator_name': f'{request.form.get("curator_name")}'}).save()
        faculty = models.Faculty(**{'faculty_name': f'{request.form.get("faculty_name")}'}).save()

        dict_student = {
            'name': f'{request.form.get("name")}',
            'group_name': [group],
            'curator_name': [curator],
            'faculty_name': [faculty]
        }
        models.Student(**dict_student).save()

        return redirect(url_for('index'))


@app.route('/edit', methods=['POST', 'GET'])
def edit():
    obj = request.form.get('edit')
    student = models.Student.objects.get(id=obj)
    return render_template('student.html', student=student)


@app.route('/update', methods=['POST', 'GET'])
def update():
    obj = request.form.get('update')
    student = models.Student.objects(id=obj).get()

    group = models.Group(**{'group_name': f'{request.form.get("group_name")}'}).save()
    curator = models.Curator(**{'curator_name': f'{request.form.get("curator_name")}'}).save()
    faculty = models.Faculty(**{'faculty_name': f'{request.form.get("faculty_name")}'}).save()

    student.name = request.form.get('name')

    student.update(**{
        'name': f'{request.form.get("name")}',
        'group_name': [group],
        'curator_name': [curator],
        'faculty_name': [faculty]
    })

    return redirect(url_for('index'))


@app.route('/delete', methods=['POST'])
def delete():
    obj = request.form.get('delete')
    models.Student.objects.get(id=obj).delete()
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)

# 2) Создать модуль, который будет заполнять базу данных случайными валидными значениями (минимум 100 студентов).

group, curator, faculty = [], [], []

for i in range(1, 6):
    group_ex = models.Group(**{'group_name': f'group {i}'}).save()
    group.append(group_ex)

for i in range(1, 6):
    curator_ex = models.Curator(**{'curator_name': f'curator {i}'}).save()
    curator.append(curator_ex)

for i in range(1, 6):
    faculty_ex = models.Faculty(**{'faculty_name': f'faculty {i}'}).save()
    faculty.append(faculty_ex)

for i in range(1, 101):

    marks_ex = {'marks': randint(2, 12)}
    marks = models.Marks(**marks_ex).save()
    marks_ex2 = {'marks': randint(2, 12)}
    marks2 = models.Marks(**marks_ex2).save()
    marks_ex3 = {'marks': randint(2, 12)}
    marks3 = models.Marks(**marks_ex3).save()

    students_ex = {
        'name': f'students {i}',
        'group_name': [choice(group)],
        'marks': [marks, marks2, marks3],
        'curator_name': [choice(curator)],
        'faculty_name': [choice(faculty)]
    }
    models.Student(**students_ex).save()

