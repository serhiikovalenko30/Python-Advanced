from mongoengine import *
import datetime

connect('blog_lesson_9')


class Tag(Document):
    title = StringField(max_length=64)


class Author(Document):
    first_name = StringField(max_length=128)
    last_name = StringField(max_length=128)
    post_count = IntField(min_value=0, default=0)


class Post(Document):
    title = StringField(max_length=255, required=True)
    content = StringField(max_length=1024)
    date = DateTimeField(default=datetime.datetime.now())
    author = ReferenceField(Author)
    views = IntField(min_value=0, default=0)
    tag = ListField(ReferenceField(Tag))
