# -*- coding: utf-8 -*-

from mongoengine import *
from config import db

class User(db.Document):
    facebook_id = db.StringField(required=True)
    email = db.StringField(required=True)
    name = db.StringField(required=True)

    @property
    def photo(self):
        url = 'http://graph.facebook.com/%s/picture'
        return url % self.facebook_id

class Feedback(db.Document):
    reposta = db.StringField(required=True)
    user = db.ReferenceField(User, required=True, reverse_delete_rule=CASCADE, dbref=False)
