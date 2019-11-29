# Написать REST для блога (использовать валидацию).
# Реализовать модель Пост (название, содержание, дата публикации, автор, кол-во просмотров, тег).
# Реализовать модель тег.
# Реализовать модель автор (имя, фамилия, кол-во публикаций автора).
# Добавить валидацию ко всем полям.
# Реализовать модуль заполнения всех полей БД валидными (адеквадными данными :) ).
# Добавить вывод всех постов по тегу, при каждом обращении к конкретному посту увеличовать кол-во просмотров на 1.
# При обращении к автору, выводить все его публикации


from flask import Flask, request, jsonify
from flask_restful import Api, Resource, abort
from resources.resource import TagResource, PostResource, AuthorResource, PostsByAuthorResource, PostsByTagResource


app = Flask(__name__)
api = Api(app)

api.add_resource(TagResource, '/tag', '/tag/<string:id>')
api.add_resource(PostResource, '/post', '/post/<string:id>')
api.add_resource(AuthorResource, '/author', '/author/<string:id>')
api.add_resource(PostsByAuthorResource, '/posts_by_author/<string: first_name')
api.add_resource(PostsByTagResource, '/posts_by_tag/<string: tag>')


if __name__ == '__main__':
    app.run()

