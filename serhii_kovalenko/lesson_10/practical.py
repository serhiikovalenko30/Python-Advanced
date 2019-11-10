# Написать REST для блога (использовать валидацию).
# Реализовать модель Пост (название, содержание, дата публикации, автор, кол-во просмотров, тег).
# Реализовать модель тег.
# Реализовать модель автор (имя, фамилия, кол-во публикаций автора).
# Добавить валидацию ко всем полям.
# Реализовать модуль заполнения всех полей БД валидными (адеквадными данными :) ).
# Добавить вывод всех постов по тегу, при каждом обращении к конкретному посту увеличовать кол-во просмотров на 1.
# При обращении к автору, выводить все его публикации


from mongoengine import *
from flask import Flask, request, jsonify
from flask_restful import Api, Resource, abort
from marshmallow import Schema, fields, ValidationError, validates
import datetime
from random import choice

app = Flask(__name__)
api = Api(app)
connect('blog_lesson_9')


""" MODELS """
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


""" SCHEMES """
class TagSchema(Schema):
    id = fields.String()
    title = fields.String()

    @validates('title')
    def validate_title(self, title):
        if '#' not in title:
            raise ValidationError('Incorrect tag')


class AuthorSchema(Schema):
    id = fields.String()
    first_name = fields.String(required=True)
    last_name = fields.String(required=True)
    post_count = fields.Integer()


class PostSchema(Schema):
    id = fields.String()
    title = fields.String(required=True)
    content = fields.String(required=True)
    date = fields.DateTime()
    author = fields.String()
    views = fields.Integer()
    tag = fields.List()


""" RESOURCES """
class TagResource(Resource):
    def get(self, id=None):
        if not id:
            objects = Tag.objects()
            return TagSchema().dump(objects, many=True)
        return TagSchema().dump(Tag.objects(id=id).get())

    def post(self):
        validity = TagSchema().validate(request.json)
        if validity:
            return validity
        obj = Tag(**request.json).save()
        return TagSchema().dump(obj)

    def put(self, id):
        obj = Tag.objects(id=id).get()
        obj.update(**request.json)
        return TagSchema().dump(obj.reload())

    def delete(self, id=None):
        if not id:
            abort(404, message='ID incorrect')
        TagSchema().dump(Tag.objects(id=id).delete())


class PostResource(Resource):
    def get(self, id=None):
        if not id:
            objects = Post.objects()
            return PostSchema().dump(objects, many=True)
        post = Post.objects(id=id).get()
        post.views += 1
        post.save()
        return PostSchema().dump(Post.objects(id=id).get())

    def post(self):
        validity = PostSchema().validate(request.json)
        if validity:
            return validity
        obj = Post(**request.json).save()
        return PostSchema().dump(obj)

    def put(self, id):
        obj = Post.objects(id=id).get()
        obj.update(**request.json)
        return PostSchema().dump(obj.reload())

    def delete(self, id=None):
        if not id:
            abort(404, message='ID incorrect')
        PostSchema().dump(Post.objects(id=id).delete())


class AuthorResource(Resource):
    def get(self, id=None):
        if not id:
            objects = Author.objects()
            return AuthorSchema().dump(objects, many=True)
        return AuthorSchema().dump(Author.objects(id=id).get())

    def post(self):
        validity = AuthorSchema().validate(request.json)
        if validity:
            return validity
        obj = Author(**request.json).save()
        return AuthorSchema().dump(obj)

    def put(self, id):
        obj = Author.objects(id=id).get()
        obj.update(**request.json)
        return AuthorSchema().dump(obj.reload())

    def delete(self, id=None):
        if not id:
            abort(404, message='ID incorrect')
        AuthorSchema().dump(Author.objects(id=id).delete())


class PostsByAuthorResource(Resource):
    def get(self, first_name=None):
        if not first_name:
            return jsonify(**{'error': 'Incorrect Author'})
        authors = Author.objects().distinct('first_name')
        if first_name not in authors:
            abort(404, message=f'Not found posts with author: {first_name}')
        author = Author.objects(first_name=first_name).get()
        posts = Post.objects(author=author)
        return PostSchema().dump(posts, many=True)


class PostsByTagResource(Resource):
    def get(self, tag):
        if not tag:
            return jsonify(**{'error': 'Incorrect tag'})
        tags = Tag.objects().distinct('title')
        if tag not in tags:
            abort(404, message=f'Not found posts with tag: {tag}')
        tag = Tag.objects(title=tag).get()
        posts = Post.objects(tag=tag)
        return PostSchema().dump(posts, many=True)


api.add_resource(TagResource, '/tag', '/tag/<string:id>')
api.add_resource(PostResource, '/post', '/post/<string:id>')
api.add_resource(AuthorResource, '/author', '/author/<string:id>')
api.add_resource(PostsByAuthorResource, '/posts_by_author/<string: first_name')
api.add_resource(PostsByTagResource, '/posts_by_tag/<string: tag>')


if __name__ == '__main__':
    app.run()


""" SEEDER """
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
