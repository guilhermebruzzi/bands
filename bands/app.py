#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
from flask import Flask, redirect, url_for, session, request, render_template
from config import app, facebook
from helpers import get_or_create_user

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/pesquisa/')
def pesquisa():
    return render_template("pesquisa.html", current_user=session['current_user'])

@app.route('/login/')
def login(next_url=None):
    facebook_url = url_for('facebook_authorized', _external=True)
    return facebook.authorize(
        callback=facebook_url
    )
    
@app.route('/login/authorized/')
@facebook.authorized_handler
def facebook_authorized(resp):
    if resp is None:
        return 'Access denied: reason=%s error=%s' % (
            request.args['error_reason'],
            request.args['error_description']
        )
    session['oauth_token'] = (resp['access_token'], '')
    me = facebook.get('/me')
    session['current_user'] = get_or_create_user(me.data)
    next_url = url_for('pesquisa')
    return redirect(next_url)


@facebook.tokengetter
def get_facebook_oauth_token():
    return session.get('oauth_token')

def run(**config):
    app.run(**config)

if __name__ == '__main__':
    run()
