#-*- coding:utf-8 -*-

import unicodedata
import re
import flask
import json
import urllib2

from flask import session

def get_slug(title):
    slug = unicodedata.normalize('NFKD', unicode(title))
    slug = slug.encode('ascii', 'ignore').lower()
    slug = re.sub(r'[^a-z0-9]+', '-', slug).strip('-')
    slug = re.sub(r'[-]+', '-', slug)
    return slug

def get_json(url):
    response = urllib2.urlopen(url)
    json_response = json.loads(response.read())
    return json_response

def get_musicians_from_opengraph(facebook_id, oauth_token):
    url_to_get_musicians = "https://graph.facebook.com/%s/music?access_token=%s" % (facebook_id, oauth_token)
    musicians = get_json(url_to_get_musicians)

    musicians_names = []
    while len(musicians["data"]) > 0:
        for music in musicians["data"]:
            if music["category"] == "Musician/band":
                musicians_names.append(music["name"])

        musicians = get_json(musicians["paging"]["next"])
    return musicians_names


def user_logged():
    return ('current_user' in flask.session.keys())


def get_current_user():
    if user_logged():
        return session['current_user']
    else:
        return None



def need_to_be_logged(handler, path="/"):
    def wrapper(*args, **kwargs):
        if not user_logged():
            return flask.redirect(path)
        return handler(*args, **kwargs)
    wrapper.__name__ = handler.__name__
    return wrapper


def need_to_be_admin(handler, path="/"):
    return handler


def prepare_post_data():
    post_data = {}
    for key in flask.request.form:
        post_data[key] = flask.request.form.getlist(key)
    return post_data

def count_tags(tags, sizes=6):
    MAX = max(tags.values()) # Needed to calculate the steps for the font-size

    STEP = MAX / sizes

    tagclouds = []

    for label, count in tags.items():
        size = count / STEP
        tagcloud = {"label": label, "size": size}
        tagclouds.append(tagcloud)

    return tagclouds
