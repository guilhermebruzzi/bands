#-*- coding:utf-8 -*-

import unicodedata
import re
from models import User, Feedback
from mongoengine.queryset import DoesNotExist

def get_slug(title):
    slug = unicodedata.normalize('NFKD', unicode(title))
    slug = slug.encode('ascii', 'ignore').lower()
    slug = re.sub(r'[^a-z0-9]+', '-', slug).strip('-')
    slug = re.sub(r'[-]+', '-', slug)
    return slug

def get_or_create_user(data):
    try:
        user = User.objects.get(facebook_id=data['id'])
    except DoesNotExist:
        user = User.objects.create(facebook_id=data['id'], email=data['email'], name=data['name'])
    return user
