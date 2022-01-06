from extensions import db, ma
from datetime import datetime
from marshmallow import fields, post_load, validate, ValidationError
from flask_login import UserMixin
import config.const as CONST
import logging

log = logging.getLogger()


# This class represents a user record in the database
class Drama(db.Model):
    __tablename__ = 'drama'
    id = db.Column(db.Integer, primary_key=True)
    person = db.Column(db.String(52))
    drama = db.Column(db.Text())
    owner = db.Column(db.String(52))


    def update(self, drama_data=None):
        print("Preparing to update drama")
        if drama_data is None:
            drama_data = {}
        self.person = drama_data.get("person", self.person)
        self.drama = drama_data.get("drama", self.password)
        db.session.add(self)
        db.session.commit()
        return self

    def delete(self):
        db.session.delete(self)
        db.session.commit()


class DramaSchema(ma.Schema):

    id = fields.Integer()
    person = fields.String(allow_none=False)
    drama = fields.String(allow_none=True)
    owner = fields.String(allow_none=False)




    @post_load
    def make_user(self, **data):
        return Drama(*data)
