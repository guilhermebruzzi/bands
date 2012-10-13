# -*- coding: utf-8 -*-

import os

from flask import Flask
from flaskext.oauth import OAuth
from flaskext.mongoengine import MongoEngine

app = Flask(__name__)
app.config.from_pyfile('app.cfg')
bd_keys = ("MONGODB_DB", "MONGODB_USERNAME", "MONGODB_PASSWORD", "MONGODB_HOST", "MONGODB_PORT")

for key in bd_keys:
    if os.environ.has_key(key):
        app.config[key] = os.environ[key]

oauth = OAuth()

facebook = oauth.remote_app('facebook',
    base_url='https://graph.facebook.com/',
    request_token_url=None,
    access_token_url='/oauth/access_token',
    authorize_url='https://www.facebook.com/dialog/oauth',
    consumer_key=app.config["FACEBOOK_APP_ID"],
    consumer_secret=app.config["FACEBOOK_APP_SECRET"],
    request_token_params={'scope': 'email'}
)

db = MongoEngine(app)
