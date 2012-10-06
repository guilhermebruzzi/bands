## -*- coding: utf-8 -*-
#
#from flask import Flask
#from flaskext.oauth import OAuth
#from flaskext.mongoengine import MongoEngine
#
#SECRET_KEY = 'development key'
#DEBUG = True
#FACEBOOK_APP_ID = '306587212773787'
#FACEBOOK_APP_SECRET = '4663b78f1079d483ed07d15ecfef01ca'
#
#
#app = Flask(__name__)
#app.debug = DEBUG
#app.secret_key = SECRET_KEY
#
#app.config.from_pyfile('app.cfg')
#
#oauth = OAuth()
#
#facebook = oauth.remote_app('facebook',
#    base_url='https://graph.facebook.com/',
#    request_token_url=None,
#    access_token_url='/oauth/access_token',
#    authorize_url='https://www.facebook.com/dialog/oauth',
#    consumer_key=FACEBOOK_APP_ID,
#    consumer_secret=FACEBOOK_APP_SECRET,
#    request_token_params={'scope': 'email'}
#)
#
#db = MongoEngine(app)
