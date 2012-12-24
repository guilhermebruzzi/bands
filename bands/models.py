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

    def __eq__(self, other):
        return self.facebook_id == other.facebook_id

    def __unicode__(self):
        return self.name

class Answer(db.EmbeddedDocument):
    answer = db.StringField(required=True)
    user = db.ReferenceField(User, required=True, dbref=False)

    def __eq__(self, other):
        return self.answer == other.answer and self.user == other.user

    def __unicode__(self):
        return self.answer

class Question(db.Document):
    slug = db.StringField(required=True)
    question = db.StringField(required=True)
    answers = db.ListField(EmbeddedDocumentField(Answer))

    def __eq__(self, other):
        return self.slug == other.slug

    def __unicode__(self):
        return self.question

class Band(db.Document):
    slug = db.StringField(required=True)
    name = db.StringField(required=True)
    aliases = db.ListField(StringField(required=True))
    users = db.ListField(ReferenceField(User, dbref=False))

    def __eq__(self, other):
        return self.slug == other.slug

    def __unicode__(self):
        return self.name
