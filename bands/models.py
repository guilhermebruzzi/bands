## -*- coding: utf-8 -*-
#
#from mongoengine import *
#from config import db
#
#class Supporter(db.Document):
#    facebook_id = db.StringField(required=True)
#    email = db.StringField(required=True)
#    name = db.StringField(required=True)
#
#    @property
#    def photo(self):
#        url = 'http://graph.facebook.com/%s/picture'
#        return url % self.facebook_id
#
#class Project(db.Document):
#    title = db.StringField(required=True)
#    slug = db.StringField(required=True)
#    description = db.StringField(required=True)
#    link = db.URLField(required=True)
#    owner = db.ReferenceField(Supporter, reverse_delete_rule=CASCADE, dbref=False)
#    supporters = db.ListField(db.ReferenceField(Supporter, dbref=False))
