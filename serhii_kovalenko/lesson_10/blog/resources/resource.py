from models.models import Post, Tag, Author
from schemes.schema import TagSchema, PostSchema, AuthorSchema

from flask_restful import Resource, abort
from flask import request, jsonify


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