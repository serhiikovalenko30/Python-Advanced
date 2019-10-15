# Cоздайте класс ПЕРСОНА с абстрактными методами, позволяющими вывести на экран информацию о персоне,
# а также определить ее возраст (в текущем году). Создайте дочерние классы:
# АБИТУРИЕНТ (фамилия, дата рождения, факультет), СТУДЕНТ (фамилия, дата рождения, факультет, курс), П
# РЕПОДАВАТЕЛЬ (фамилия, дата рождения, факультет, должность, стаж),
# со своими методами вывода информации на экран и определения возраста.
# Создайте список из n персон, выведите полную информацию из базы на экран, а также организуйте поиск персон,
# чей возраст попадает в заданный диапазон.

from abc import ABC, abstractmethod
from datetime import date, datetime


class Person(ABC):
    PERSON_LIST = []

    def __init__(self, last_name, birthday_day, faculty,
                 course='None', position='None', experience='None'):
        self.last_name = last_name
        self.birthday_day = birthday_day
        self.faculty = faculty

        self.course = course
        self.position = position
        self.experience = experience

        Person.PERSON_LIST.append(self)

    @abstractmethod
    def get_person_info(self):
        raise NotImplementedError()

    @classmethod
    def find_person(cls, start, end):
        person_list = []
        print(f'Person whose age falls within a given range {start} and {end}:')
        for i in range(len(cls.PERSON_LIST)):
            if start <= cls.PERSON_LIST[i].get_age() <= end:
                cls.PERSON_LIST[i].get_person_info()
                person_list.append(cls.PERSON_LIST[i].__dict__)
        return person_list

    def get_age(self):
        if date.today().month >= datetime.strptime(self.birthday_day, '%d-%m-%Y').date().month:
            return date.today().year - datetime.strptime(self.birthday_day, '%d-%m-%Y').date().year
        return date.today().year - datetime.strptime(self.birthday_day, '%d-%m-%Y').date().year - 1


class Enrollee(Person):
    def __init__(self, last_name, birthday_day, faculty):
        super().__init__(last_name=last_name, birthday_day=birthday_day, faculty=faculty)

    def get_person_info(self):
        print(f'{self.__class__.__name__}:\n'
              f'Last Name - {self.last_name}\n'
              f'Birthday day - {self.birthday_day}\n'
              f'Faculty - {self.faculty }')


class Student(Person):
    def __init__(self, last_name, birthday_day, faculty, course):
        super().__init__(last_name=last_name, birthday_day=birthday_day, faculty=faculty,
                         course=course)

    def get_person_info(self):
        print(f'{self.__class__.__name__}:\n'
              f'Last Name - {self.last_name}\n'
              f'Birthday day - {self.birthday_day}\n'
              f'Faculty - {self.faculty}\n'
              f'Course - {self.course}')


class Teacher(Person):
    def __init__(self, last_name, birthday_day, faculty, position, experience):
        super().__init__(last_name=last_name, birthday_day=birthday_day, faculty=faculty,
                         position=position, experience=experience)

    def get_person_info(self):
        print(f'{self.__class__.__name__}:\n'
              f'Last Name -  {self.last_name}\n'
              f'Birthday day - {self.birthday_day}\n'
              f'Faculty - {self.faculty}\n'
              f'Position - {self.position}\n'
              f'Experience - {self.experience}')


Enrollee_1 = Enrollee('Kovalenko', '31-07-1989', 'a')
Enrollee_2 = Enrollee('Kovalenko', '31-07-2010', 'b')
Teacher_1 = Teacher('Kovalenko', '31-07-1982', 'c', 'director', '4')
Student_1 = Student('Kovalenko', '31-07-2002', 'd', '2')

for person in Person.PERSON_LIST:
    person.get_person_info()

Person.find_person(5, 22)

# Создать подобие социальной сети. Описать классы, которые должны выполнять соответствующие функции
# (Предлагаю насследовать класс авторизации от класса регистрации).
# Добавить проверку на валидность пароля (содержание символов и цифр), проверка на уникальность логина пользователя.
# Человек заходит, и имеет возможность зарегистрироваться (ввод логин, пароль, потдверждение пароля),
# далее входит в свою учетную запись. Добавить возможность выхода из учетной записи, и вход в новый аккаунт.
# Создать класс User, котоырй должен разделять роли обычного пользователя и администратора.
# При входе под обычным пользователем мы можем добавить новый пост, с определённым содержимим,
# так же пост должен содержать дату публикации.
# Под учётной записью администратора мы можем увидеть всех пользователей нашей системы, дату их регистрации, и их посты.

import shelve
import time

user_password_db = 'user_password_db'
user_registration_date_db = 'user_registration_date_db'
user_post_db = 'user_post_db'


class Registration:
    @classmethod # возможность зарегистрироваться (ввод логин, пароль, потдверждение пароля)
    def registration(cls):
        login = input('Please enter login: ')
        password = input('Please enter password: ')
        repeat_password = input('Please repeat password: ')

        if repeat_password != password:
            print('Passwords do not match. Try again')
        elif not cls.password_validator(password):
            print('Password incorrect. Try again')
        elif cls.login_validator(login):
            print('Login already exists. Try again')
        else:
            with shelve.open(user_password_db) as db:
                db[login] = password
            with shelve.open(user_registration_date_db) as db:
                db[login] = time.time()

            # после корректной регистрации я сразу авторизируюсь
            return Authorization.authorization(login, password)

    @classmethod # проверку на валидность пароля (содержание символов и цифр)
    def password_validator(cls, password):
        if any(c.isdigit() for c in password) and any(c.isalpha() for c in password):
            return True
        return False

    @classmethod # проверка на уникальность логина пользователя
    def login_validator(cls, login):
        with shelve.open(user_password_db) as db:
            return db.get(login, False)


class Authorization(Registration):
    @classmethod # входит в свою учетную запись
    def authorization(cls, login=None, password=0):
        if password == 0:
            login = input('Please enter login: ')
            password = input('Please enter password: ')
            with shelve.open(user_password_db) as db:
                if db.get(login, "Undefined") == 'Undefined':
                    print(f'Login does not exist Try again')
                    return Authorization.authorization()
                else:
                    if db[login] == password:
                        print(f'You are logged in as "{login}"')
                        return User(login)
                    else:
                        print(f'Incorrect password. Try again')
                        return Authorization.authorization()
        else:
            with shelve.open(user_password_db) as db:
                if db[login] == password:
                    print(f'You are logged in as "{login}"')
                    return User(login, 1)
                return print('Incorrect login or password')

    @classmethod # возможность выхода из учетной записи
    def quit(cls):
        print('You left.')
        Authorization.authorization()

    @classmethod # вход в новый аккаунт
    def change_account(cls):
        print('Change account')
        Authorization.authorization()


class User(Authorization):
    user_posts = {}

    # роли обычного пользователя и администратора
    def __init__(self, login, admin=False):
        self._login = login
        self._admin = admin

    def _get_admin(self):
        return self._admin

    # добавить новый пост, с определённым содержимим, так же пост должен содержать дату публикации
    def create_post(self):
        title = input('Title: ')
        content = input('Content: ')
        date = time.time()

        with shelve.open(user_post_db) as db:
            id_post = str(len(db))
            db[id_post] = f'Title: {title}. Content: {content}. Date: {date}'

        if self._login in User.user_posts:
            key = User.user_posts.pop(f'{self._login}')
            key.append(id_post)
            User.user_posts[f'{self._login}'] = key
        else:
            User.user_posts[f'{self._login}'] = [id_post]

    # мы можем увидеть всех пользователей нашей системы, дату их регистрации, и их посты
    def get_login(self):
        if not self._get_admin():
            return print('Not Admin')
        else:
            with shelve.open(user_password_db) as db:
                for i in db.items():
                    print(i)

    def get_post(self):
        if not self._get_admin():
            return print('Not Admin')
        else:
            with shelve.open(user_post_db) as db:
                print(User.user_posts)
                for i in db.items():
                    print(i)

    def get_date_of_registration(self):
        if not self._get_admin():
            return print('Not Admin')
        else:
            with shelve.open(user_registration_date_db) as db:
                for i in db.items():
                    print(i)


while True:
    inp = input("Please choose action 1-'Registration' or 2-'Authorization'. ")
    if inp == '1':
        user = Registration.registration()
        if user:
            break
    elif inp == '2':
        user = Authorization.authorization()
        if user:
            break
    else:
        print('Incorrect choose. Try again')


while True:
    inp_2 = input("Please choose action \n"
                  "1-'Create Post' or 2-'Change Account' or 3-'Quit'. \n"
                  "For Admin: \n"
                  "4-'Get Users' or 5-'Get users posts' or 6-'get users date of registration': \n")
    if inp_2 == '1':
        user.create_post()
    elif inp_2 == '2':
        Authorization.change_account()
    elif inp_2 == '3':
        Authorization.quit()
    elif inp_2 == '4':
        user.get_login()
    elif inp_2 == '5':
        user.get_post()
    elif inp_2 == '6':
        user.get_date_of_registration()
    else:
        print('Incorrect choose. Try again')
