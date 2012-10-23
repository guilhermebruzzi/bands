#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
from flask import Flask, redirect, url_for, session, request, render_template
from config import app, facebook
from helpers import user_logged
from models import Answer
from controllers import get_or_create_user, get_or_create_questions, validate_answers, create_answers

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/pesquisa/', methods=['GET', 'POST'])
def pesquisa():
    if not user_logged():
        return redirect(url_for('index'))

    current_user=session['current_user']

    post_data = request.form

    #  Apagar depois
    questions = get_or_create_questions(["Teste?"])
    answer = Answer(answer="Teste1", user=current_user)
    questions[0].answers = [answer]
    questions[0].save()
    #  Apagar depois

    if request.method == 'POST':
        if validate_answers(post_data):
            create_answers(post_data)

    return render_template('pesquisa.html', current_user=current_user, questions=questions, post_data=post_data)

@app.route('/login/')
def login():
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

    return redirect(url_for('pesquisa'))


@facebook.tokengetter
def get_facebook_oauth_token():
    return session.get('oauth_token')


if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
