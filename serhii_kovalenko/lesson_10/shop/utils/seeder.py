from models.models import Category, Item
from random import choice, randint

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
