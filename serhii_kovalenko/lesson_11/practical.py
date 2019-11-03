# Написать бота-консультанта, который будет собирать информацию с пользователя
# (его ФИО, номер телефона, почта, адресс, пожелания). Записывать сформированную заявку в БД (по желанию SQl/NOSQL).

import telebot
import config as c
import sqlite3

db_name = 'anketa.db'

class ContextManagerForSQL:

    def __init__(self, db_name):
        self._file = sqlite3.connect(db_name)

    def __enter__(self):
        return self._file.cursor()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._file.commit()
        self._file.close()


def get_information_from_form(id):
    sql_query = """select * from user_anketa where id = ?"""
    with ContextManagerForSQL(db_name) as db:
        if db.execute(sql_query, [id]).fetchone() is None:
            return False
        return [x for x in db.execute(sql_query, [id]).fetchone() if x is not None]


def set_id(id):
    sql_query = """insert into user_anketa (id) values (?)"""
    with ContextManagerForSQL(db_name) as db:
        db.execute(sql_query, [id])


def set_name(id, name):
    sql_query = """update user_anketa set name = ? where id = ?"""
    with ContextManagerForSQL(db_name) as db:
        db.execute(sql_query, [name, id])


def set_phone(id, phone):
    sql_query = """update user_anketa set phone = ? where id = ?"""
    with ContextManagerForSQL(db_name) as db:
        db.execute(sql_query, [phone, id])


def set_email(id, email):
    sql_query = """update user_anketa set email = ? where id = ?"""
    with ContextManagerForSQL(db_name) as db:
        db.execute(sql_query, [email, id])


def set_address(id, address):
    sql_query = """update user_anketa set address = ? where id = ?"""
    with ContextManagerForSQL(db_name) as db:
        db.execute(sql_query, [address, id])


bot = telebot.TeleBot(c.TOKEN)


@bot.message_handler(commands=['start'])
def start(message):
    set_id(message.chat.id)
    bot.send_message(message.chat.id, 'write your name')


@bot.message_handler(func=lambda message: len(get_information_from_form(message.chat.id)) == 1)
def get_phone(message):
    set_name(message.chat.id, message.text)
    bot.send_message(message.chat.id, 'write your phone number')


@bot.message_handler(func=lambda message: len(get_information_from_form(message.chat.id)) == 2)
def get_email(message):
    set_phone(message.chat.id, message.text)
    bot.send_message(message.chat.id, 'write your email')


@bot.message_handler(func=lambda message: len(get_information_from_form(message.chat.id)) == 3)
def get_address(message):
    set_email(message.chat.id, message.text)
    bot.send_message(message.chat.id, 'write your address')


@bot.message_handler(func=lambda message: len(get_information_from_form(message.chat.id)) == 4)
def fin(message):
    set_address(message.chat.id, message.text)
    bot.send_message(message.chat.id,
                     f'Thank. I remember Your. \n'
                     f'Name: {get_information_from_form(message.chat.id)[1]}\n'
                     f'Phone: {get_information_from_form(message.chat.id)[2]}\n'
                     f'Email: {get_information_from_form(message.chat.id)[3]}\n'
                     f'Address: {get_information_from_form(message.chat.id)[4]}\n')


bot.polling(none_stop=True)
