#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
from flask import Flask, redirect, url_for, session, request, render_template
from config import app, facebook
from helpers import get_or_create_user#, validate_answers, get_or_create_answers, get_or_create_questions

@app.route('/')
def index():
    return render_template("index.html")

#def add_answers(request, questions):
#    (error, msg_error) = validate_answers(request)
#    if request.method == 'POST' and not error:
#        get_or_create_answers(request)
#        return render_template('pesquisa_success.html', current_user=session['current_user'])
#    elif error:
#        return render_template('pesquisa.html', current_user=session['current_user'], questions=questions, msg_error=msg_error)
#    return render_template('pesquisa.html', current_user=session['current_user'], questions=questions)

@app.route('/pesquisa/', methods=['GET', 'POST'])
def pesquisa():
#    questions_text = [""]
#    questions = get_or_create_questions(questions_text)
#    return add_answers(request, questions)
    return render_template('pesquisa.html', current_user=session['current_user'])

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
