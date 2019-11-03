# Написать контекстный менеджер для работы с SQLite DB.

import sqlite3


class ContextManagerForSQL:

    def __init__(self, db_name):
        self._file = sqlite3.connect(db_name)

    def __enter__(self):
        return self._file.cursor()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._file.commit()
        self._file.close()


# Создать базу данных студентов.
# У студента есть факультет, группа, оценки, номер студенческого билета.
# Написать программу, с двумя ролями: Администратор, Пользователь.
# Администратор может добавлять, изменять существующих студентов.
# Пользователь может получать список отличников, список всех студентов, искать студентов по номеру студенческого,
# получать полную информацию о конкретном студенте(включая оценки, факультет)


class Admin:

    def __init__(self, db_name):
        self._db_name = db_name

    def add_student(self, first_name, last_name, id_student_card, id_faculty, id_group):
        first_name, last_name, id_student_card, id_faculty, id_group = \
            first_name, last_name, id_student_card, id_faculty, id_group
        sql_query = """ insert into students 
                        (first_name, last_name, id_student_card, id_faculty, id_group)
                        values (?, ?, ?, ?, ?)
                    """
        with ContextManagerForSQL(self._db_name) as db:
            db.execute(sql_query, [first_name, last_name, id_student_card, id_faculty, id_group])

    def change_student(self, id, first_name, last_name, id_student_card, id_faculty, id_group):
        sql_query_find = """ select *
                             from students
                             where id = ?
                         """
        with ContextManagerForSQL(self._db_name) as db:
            result = db.execute(sql_query_find, [id]).fetchone()
        if not result:
            print(f'Student with id-{id} does not exist')

        first_name, last_name, id_student_card, id_faculty, id_group = \
            first_name, last_name, id_student_card, id_faculty, id_group
        sql_query_update = """ update students 
                               set first_name = ?, last_name = ?, id_student_card = ?, id_faculty = ?, id_group = ?
                               where id = ?
                           """
        with ContextManagerForSQL(self._db_name) as db:
            db.execute(sql_query_update, [first_name, last_name, id_student_card, id_faculty, id_group, id])


class User:

    def __init__(self, db_name):
        self._db_name = db_name

    def get_list_of_excellent_students(self):
        sql_query = """ select first_name, last_name, avg(value) as total_marks 
                        from students
                        left join marks on marks.id = students.id
                        group by first_name, last_name
                        order by avg(value) desc
                    """
        with ContextManagerForSQL(self._db_name) as db:
            print(db.execute(sql_query).fetchone())

    def get_student_list(self):
        sql_query = """ select first_name, last_name
                        from students
                    """
        with ContextManagerForSQL(self._db_name) as db:
            print(db.execute(sql_query).fetchall())

    def find_student(self, id_student_card):
        sql_query = """ select first_name, last_name 
                        from students 
                        where id_student_card = ?
                    """
        with ContextManagerForSQL(self._db_name) as db:
            print(db.execute(sql_query, [id_student_card]).fetchall())

    def get_student_info(self, id_student_card):
        sql_query = """ select *
                        from students 
                        left join faculty on faculty.id = students.id
                        left join student_card on student_card.id = students.id
                        left join marks on marks.id = students.id
                        left join [group] on [group].id = students.id
                        where id_student_card = ?
                    """
        with ContextManagerForSQL(self._db_name) as db:
            print(db.execute(sql_query, [id_student_card]).fetchall())


class Authorization:

    def __init__(self, db_name):
        self._db_name = db_name

    def login(self):
        login = input('Enter your login: \n')
        sql_query = """ select login
                        from users
                        where login = ?
                    """
        with ContextManagerForSQL(self._db_name) as db:
            result_login = db.execute(sql_query, [login]).fetchone()

        if not result_login:
            print('Login field')
        else:
            password = input('Enter your password: \n')
            sql_query = """ select password 
                            from users
                            where login = ?
                        """
            with ContextManagerForSQL(self._db_name) as db:
                result_password = db.execute(sql_query, [login]).fetchone()
            if not password == result_password[0]:
                print('Incorrect password')
            else:
                sql_query = """ select title
                                from users
                                left join role on users.role_id = role.id
                                where login = ?
                            """
                with ContextManagerForSQL(self._db_name) as db:
                    title = db.execute(sql_query, [login]).fetchone()
                    return title


db = 'db_students.db'
login = Authorization(db).login()

if login:
    if login[0] == 'admin':
        print('Hi admin')
        admin = Admin(db)

        user_input = int(input('Enter 1 for add student\n'
                               'Enter 2 for change students\n'))
        if user_input == 1:
            first_name = input('Enter first name: ')
            last_name = input('Enter last name: ')
            id_student_card = int(input('Enter student card id: '))
            id_faculty = int(input('Enter student faculty id: '))
            id_group = int(input('Enter student group id: '))
            admin.add_student(first_name, last_name, id_student_card, id_faculty, id_group)
        elif user_input == 2:
            id = int(input('Enter student id: '))
            first_name = input('Enter first name: ')
            last_name = input('Enter last name: ')
            id_student_card = int(input('Enter student card id: '))
            id_faculty = int(input('Enter student faculty id: '))
            id_group = int(input('Enter student group id: '))
            admin.change_student(id, first_name, last_name, id_student_card, id_faculty, id_group)
        else:
            print('Incorrect enter')

    elif login[0] == 'reader':
        print('Hi user')
        user = User(db)

        user_input = int(input('Enter 1 for find student\nEnter 2 for list excellent students\n'
                               'Enter 3 for students info\nEnter 4 for students list\n'))
        if user_input == 1:
            student_card = input('Enter number student card: ')
            user.find_student(student_card)
        elif user_input == 2:
            user.get_list_of_excellent_students()
        elif user_input == 3:
            student_card = input('Enter number student card: ')
            user.get_student_info()
        elif user_input == 4:
            user.get_student_list()
        else:
            print('Incorrect enter')
