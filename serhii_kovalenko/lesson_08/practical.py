# 1) Создать базу данных товаров, у товара есть: Категория (связанная таблица), название,
# есть ли товар в продаже или на складе, цена, кол-во единиц.
# Создать html страницу.
# На первой странице выводить ссылки на все категории,
# при переходе на категорию получать список всех товаров в наличии ссылками,
# при клике на товар выводить его цену, полное описание и кол-во единиц в наличии.

from flask import Flask, render_template, request, redirect, url_for
import sqlite3


class ContextManagerForSQL:

    def __init__(self, db_name):
        self._file = sqlite3.connect(db_name)

    def __enter__(self):
        return self._file.cursor()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._file.commit()
        self._file.close()


app = Flask(__name__)
db_name = 'store.db'


@app.route('/')
def category():
    sql_query = """select id, category_name from category"""
    with ContextManagerForSQL(db_name) as db:
        execute = db.execute(sql_query).fetchall()
    category = {key: value for (key, value) in execute}
    return render_template('index.html', category=category)


@app.route("/goods/<id>")
def goods(id):
    sql_query = """select id, name from goods where category_id = ? and in_stock > 0"""
    with ContextManagerForSQL(db_name) as db:
        execute = db.execute(sql_query, [id]).fetchall()
    goods = {key: value for (key, value) in execute}
    return render_template('goods.html', goods=goods)


@app.route("/goods_detail/<id>")
def goods_detail(id):
    sql_query = """select name, price, count from goods where id = ?"""
    with ContextManagerForSQL(db_name) as db:
        execute = db.execute(sql_query, [id]).fetchone()
    return render_template('goods_detail.html', goods_detail=execute)

# 2) Создать страницу для администратора, через которую он может добавлять новые товары и категории.

@app.route('/admin')
def admin():
    sql_query = """select id, category_name from category"""
    with ContextManagerForSQL(db_name) as db:
        execute = db.execute(sql_query).fetchall()
    category = {key: value for (key, value) in execute}
    return render_template('admin.html', category=category)


@app.route('/add_category', methods=['POST'])
def add_category():
    category_name = request.form.get('category')
    sql_query = """insert into category (category_name) values (?)"""
    with ContextManagerForSQL(db_name) as db:
        db.execute(sql_query, [category_name])

    return redirect(url_for('admin'))


@app.route('/add_good', methods=['POST'])
def add_good():
    name = request.form.get('name')
    category_id = request.form.get('category_id')
    in_stock = request.form.get('in_stock')
    price = request.form.get('price')
    count = request.form.get('count')

    sql_query = """insert into goods (name, category_id, in_stock, price, count) values (?, ?, ?, ?, ?)"""
    with ContextManagerForSQL(db_name) as db:
        db.execute(sql_query, [name, category_id, in_stock, price, count])

    return redirect(url_for('admin'))


if __name__ == '__main__':
    app.run(debug=True)