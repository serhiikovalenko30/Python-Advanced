from marshmallow import Schema, fields, validates, ValidationError
from models.models import *


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
