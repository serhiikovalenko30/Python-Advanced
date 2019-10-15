# 1) Создать декоратор, который будет запускать функцию в отдельном
# потоке. Декоратор должен принимать следующие аргументы:
# название потока, является ли поток демоном.

from threading import Thread


def decorator_one(fn):
    def wrapper(name, is_daemon):
        Thread(target=fn, name=name, daemon=is_daemon).start()
    return wrapper


# 2) Создать функцию, которая будет скачивать файл из интернета по
# ссылке, повесить на неё созданный декоратор. Создать список из 10
# ссылок, по которым будет происходить скачивание. Создать список
# потоков, отдельный поток, на каждую из ссылок. Каждый поток
# должен сигнализировать, о том, что, он начал работу и по какой
# ссылке он работает, так же должен сообщать когда скачивание
# закончится.

import urllib.request

url_list = [
    'https://github.com/serhiikovalenko30/Python-Advanced/tree/master/serhii_kovalenko/lesson_01',
    'https://github.com/serhiikovalenko30/Python-Advanced/tree/master/serhii_kovalenko/lesson_02',
    'https://github.com/serhiikovalenko30/Python-Advanced/tree/master/serhii_kovalenko/lesson_03'
]
thread_list = [
    'thread_01',
    'thread_02',
    'thread_03'
]


def decorator_two(fn):
    def wrapper(name, is_daemon, *args):
        Thread(target=fn, args=(*args,), name=name, daemon=is_daemon).start()
    return wrapper


@decorator_two
def download(url, thread_name):
    print(f'Thread "{thread_name}" for link "{url}" start')
    urllib.request.urlretrieve(url)
    print(f'Thread "{thread_name}" for link "{url}" end')


for i in range(len(url_list)):
    download(thread_list[i], False, url_list[i], thread_list[i])


# 3) Написать свой контекстный менеджер для работы с файлами.

class ContextManagerForFile:

    def __init__(self, filename, method):
        self._file = open(filename, method)

    def __enter__(self):
        return self._file

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._file.close()


with ContextManagerForFile('file.txt', 'w') as file:
    file.write('Hello')

with ContextManagerForFile('file.txt', 'r') as file:
    for i in file:
        print(i)


# 4) Дополнение к предыдущей работе с соц. Сетью. Все хранение
# данных пользователей реализовать на основе модуля shelve.

# \\lesson_4\practical.py

