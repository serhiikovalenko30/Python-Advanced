# Реализовать REST интернет магазина.
# Модель товар (цена, доступность, кол-во доступных единиц, категория, кол-во просмотров),
# Категория (описание, название). При обращении к конкретному товару увеличивать кол-во просмотров на 1.
# Добавить модуль для заполнения БД валидными данными. Реализовать подкатегории ( доп. Бал).
# Добавить роут, который выводят общую стоимость товаров в магазине.

from flask import Flask, request, jsonify
from flask_restful import Api, Resource, abort
from resources.resource import StoreResource, TotalCostResource


app = Flask(__name__)
api = Api(app)

api.add_resource(StoreResource, '/shop', '/shop/<string:id>')
api.add_resource(TotalCostResource, '/total_cost')


if __name__ == '__main__':
    app.run()


