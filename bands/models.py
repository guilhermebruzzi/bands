# -*- coding: utf-8 -*-

import time
from datetime import datetime
from mongoengine import *
from config import db

class User(db.Document):
    facebook_id = db.StringField(required=True)
    email = db.StringField(required=True)
    name = db.StringField(required=True)
    tipo = db.StringField(required=False)    # musico, fa, produtor, etc

    @property
    def photo(self):
        url = 'http://graph.facebook.com/%s/picture'
        return url % self.facebook_id

    def __eq__(self, other):
        return self.facebook_id == other.facebook_id

    def __unicode__(self):
        return self.name

class Newsletter(db.Document):
    option = db.BooleanField(required=True) #  Sim ou Nao
    tipo = db.StringField(required=True)  # Shows Locais, Meus Shows, etc..
    user = db.ReferenceField(User, required=True, dbref=False)

    def __eq__(self, other):
        return self.user == other.user and self.option == other.option and self.tipo == other.tipo

    def __unicode__(self):
        return u"%s - %s - %s" % (self.user, self.tipo, u"Sim" if self.option else u"Não")

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

class Location(db.Document):
    name = db.StringField(required=True)
    slug = db.StringField(required=True)
    city = db.StringField(required=True)
    street = db.StringField(required=False)
    postalcode = db.StringField(required=False)
    website = db.StringField(required=False)
    phonenumber = db.StringField(required=False)
    image = db.StringField(required=False)

    def __eq__(self, other):
        return self.slug == other.slug

    def __unicode__(self):
        return self.name

class Show(db.Document):
    slug = db.StringField(required=True)
    title = db.StringField(required=True)
    artists_slug = db.ListField(StringField())
    attendance_count = db.IntField(min_value=0, required=False, default=0)
    cover_image = db.StringField(required=False)
    description = db.StringField(required=False)
    datetime_usa = db.StringField(required=False)
    location = db.ReferenceField(Location, required=False, dbref=False)
    website = db.StringField(required=False)

    artists_list = None
    @property
    def artists(self):
        if not self.artists_list is None:
            return self.artists_list
        return Band.objects.filter(slug__in=self.artists_slug)

    @property
    def datetime(self):
        return datetime.strftime(datetime.strptime(self.datetime_usa[:19], "%Y-%m-%d %H:%M:%S"), '%d/%m/%Y %H:%M:%S')

    def __eq__(self, other):
        return self.slug == other.slug

    def __unicode__(self):
        return self.title

class Band(db.Document):
    slug = db.StringField(required=True)
    name = db.StringField(required=True)
    aliases = db.ListField(StringField(required=True))
    users = db.ListField(ReferenceField(User, dbref=False))
    shows = db.ListField(ReferenceField(Show, dbref=False))
    musicians = db.ListField(ReferenceField(User, dbref=False))

    def __eq__(self, other):
        return self.slug == other.slug

    def __unicode__(self):
        return self.name
