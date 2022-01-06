from extensions import db, ma
from datetime import datetime
from marshmallow import fields, post_load, validate, ValidationError
from flask_login import UserMixin
import config.const as CONST
import logging

log = logging.getLogger()


# This class represents a user record in the database
class User(UserMixin, db.Model):
    __tablename__ = 'Users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(52))
    password = db.Column(db.String(52))

    def update(self, user_data=None):
        print("Preparing to update user")
        if user_data is None:
            user_data = {}
        self.username = user_data.get("username", self.username)
        self.password = user_data.get("password", self.password)
        db.session.add(self)
        db.session.commit()
        return self

    def delete(self):
        db.session.delete(self)
        db.session.commit()


class UserSchema(ma.Schema):
    class Meta:
        # load_only specifies a list of fields that will only be loaded and never serialized for outputting to a user
        load_only = ['password']

    id = fields.Integer()
    username = fields.String(allow_none=True)
    password = fields.String(allow_none=True)




    @post_load
    def make_user(self, data, **kwargs):
        return User(**data)
