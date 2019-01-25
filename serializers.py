from flask_marshmallow import Marshmallow
from marshmallow_sqlalchemy import ModelSchema
from marshmallow import fields, post_dump, pre_dump
from models import User,Post
try:
    from __main__ import ma
except:
    from app import ma


class PostSchema(ma.ModelSchema):
    #users=fields.Nested(UserSchema, many=True)
    class Meta:
        # Fields to expose
        model=Post
        
class UserSchema(ma.ModelSchema):
    posts=fields.Nested(PostSchema, many=True)
    class Meta:
        # Fields to expose
        model=User