# Реализовать REST интернет магазина.
# Модель товар (цена, доступность, кол-во доступных единиц, категория, кол-во просмотров),
# Категория (описание, название). При обращении к конкретному товару увеличивать кол-во просмотров на 1.
# Добавить модуль для заполнения БД валидными данными. Реализовать подкатегории ( доп. Бал).
# Добавить роут, который выводят общую стоимость товаров в магазине.

from mongoengine import *
from flask import Flask, request, jsonify
from flask_restful import Api, Resource, abort
from marshmallow import Schema, fields
from random import choice, randint

app = Flask(__name__)
api = Api(app)
connect('shop_lesson_9')


""" MODELS """
class Category(Document):
    title = StringField(max_length=255, required=True)
    description = StringField(max_length=512)
    subcategory = ListField(ReferenceField('self'))


class Item(Document):
    title = StringField(max_length=128)
    category = ReferenceField(Category)
    is_availability = BooleanField(default=False)
    price = IntField(min_value=0, default=0)
    count = IntField(min_value=0, default=0)
    views = IntField(min_value=0, default=0)


""" SCHEMES """
class CategorySchema(Schema):
    title = fields.String()
    description = fields.String()
    subcategory = fields.List()


class ItemSchema(Schema):
    id = fields.String()
    title = fields.String(required=True)
    category = fields.String()
    is_availability = fields.Bool()
    price = fields.Integer()
    count = fields.Integer()
    views = fields.Integer()


""" RESOURCES """
class TotalCostResource(Resource):
    def get(self):
        total_cost = 0
        items = Item.objects.only('price', 'count')
        for item in items:
            total_cost += item.price * item.count
        return jsonify(**{'total_cost': total_cost})


class StoreResource(Resource):
    def get(self, id=None):
        if not id:
            objects = Item.objects
            return ItemSchema().dump(objects, many=True)
        item = Item.objects(id=id).get()
        item.views += 1
        item.save()
        return ItemSchema().dump(Item.objects(id=id).get())

    def post(self):
        validity = ItemSchema().validate(request.json)
        if validity:
            return validity
        item = Item(**request.json).save()
        return ItemSchema().dump(item)

    def put(self, id):
        obj = Item.objects(id=id).get()
        obj.update(**request.json)
        return ItemSchema().dump(obj.reload())

    def delete(self, id):
        if not id:
            abort(404, message='ID incorrect')
        ItemSchema().dump(Item.objects(id=id).delete())


api.add_resource(StoreResource, '/shop', '/shop/<string:id>')
api.add_resource(TotalCostResource, '/total_cost')


if __name__ == '__main__':
    app.run()


""" SEEDER """
category = []

for i in range(1, 6):
    category_ex = Category(**{
        'title': f'category number {i}',
        'description': f'description by category number {i}',
    }).save()
    category.append(category_ex)

for i in range(1, 11):
    item_ex = {
        'title': f'item number {i}',
        'category': choice(category),
        'is_availability': True,
        'price': randint(100, 1000),
        'count': randint(10, 50)
    }
    Item(**item_ex).save()