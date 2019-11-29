from models.models import Tag, Author, Post
from random import choice

tag = []
author = []

for i in range(1, 6):
    tag_ex = Tag(**{'title': f'#tag{i}'}).save()
    tag.append(tag_ex)

for i in range(1, 3):
    author_ex = Author(**{
        'first_name': f'First Name {i}',
        'last_name': f'Last Name {i}'
    }).save()
    author.append(author_ex)

for i in range(1, 11):
    post_ex = {
        'title': f'title by post number {i}',
        'content': f'content by post number {i}',
        'author': choice(author),
        'tag': [choice(tag), choice(tag)]
    }
    Post(**post_ex).save()
