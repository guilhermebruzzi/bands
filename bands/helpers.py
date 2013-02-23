#-*- coding:utf-8 -*-

import unicodedata
import re
import flask
import json
import urllib2


from flask import session, render_template, request
from config import get_app

app = get_app()

def render_template(url, **data):
    if not "debug" in data.keys():
        data["debug"] = app.config["DEBUG"]

    return flask.render_template(url, **data)

def get_client_ip():
    if not request.headers.getlist("X-Forwarded-For"):
        ip = request.remote_addr
    else:
        ip = request.headers.getlist("X-Forwarded-For")[0]
    return ip

def get_current_city(ip):
    if ip == '127.0.0.1':
        return 'Rio de Janeiro'
    city = urllib2.urlopen('http://api.hostip.info/get_html.php?ip=%s&position=true' % ip).read()
    if city:
        return city
    return 'Rio de Janeiro'

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


def user_logged():
    return ('current_user' in flask.session.keys())


def get_current_user():
    if user_logged():
        return session['current_user']
    else:
        return None

def has_cookie_login(req):
    is_user_logged = True if req.cookies.get('user_logged') else False
    return is_user_logged

def set_cookie_login(resp):
    current_user = get_current_user()
    resp.set_cookie('user_logged', current_user.facebook_id)

def delete_cookie_login(resp):
    resp.delete_cookie('user_logged')


def need_to_be_logged(handler, path="/"):
    def wrapper(*args, **kwargs):
        if not user_logged():
            return flask.redirect(path)
        return handler(*args, **kwargs)

    wrapper.__name__ = handler.__name__
    return wrapper


def need_to_be_admin(handler, path="/"):
    def wrapper(*args, **kwargs):
        if not user_logged():
            return flask.redirect(path)
        current_user = get_current_user()
        admins_facebook_ids = ['100000387455926', '100000002085352', '1784830537', '100002399821369'] #  Dudu, Guilherme, Guto, Rodrigo
        if not current_user.facebook_id in admins_facebook_ids:
            return flask.redirect(path)
        return handler(*args, **kwargs)

    wrapper.__name__ = handler.__name__
    return wrapper


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
