#-*- coding:utf-8 -*-

import unicodedata
import re
import flask


def get_slug(title):
    slug = unicodedata.normalize('NFKD', unicode(title))
    slug = slug.encode('ascii', 'ignore').lower()
    slug = re.sub(r'[^a-z0-9]+', '-', slug).strip('-')
    slug = re.sub(r'[-]+', '-', slug)
    return slug


def user_logged():
    return ('current_user' in flask.session.keys())


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
        if len(post_data[key]) == 1:
            post_data[key] = post_data[key][0]
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