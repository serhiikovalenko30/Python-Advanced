from marshmallow import Schema, fields, validates, ValidationError
from models.models import *


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
