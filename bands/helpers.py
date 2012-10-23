#-*- coding:utf-8 -*-

import unicodedata
import re
from flask import session

def get_slug(title):
    slug = unicodedata.normalize('NFKD', unicode(title))
    slug = slug.encode('ascii', 'ignore').lower()
    slug = re.sub(r'[^a-z0-9]+', '-', slug).strip('-')
    slug = re.sub(r'[-]+', '-', slug)
    return slug

def user_logged(session_instance=None):
    if session_instance == None:
        session_instance = session
    return ('current_user' in session_instance.keys())

