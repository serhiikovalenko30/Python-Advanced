from mongoengine import *

connect('shop_lesson_9')


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
