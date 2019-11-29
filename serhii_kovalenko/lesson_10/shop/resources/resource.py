from models.models import Item
from schemes.schema import ItemSchema

from flask_restful import Resource, abort
from flask import request, jsonify


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
