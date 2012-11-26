#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
from flask import Flask, redirect, url_for, session, request, render_template, abort, make_response
from config import get_app, facebook, MAIN_QUESTIONS, QUESTIONS_PESQUISA, project_root
from helpers import user_logged, prepare_post_data, need_to_be_logged, need_to_be_admin
from controllers import get_or_create_user, validate_answers, save_answers, get_all_questions_and_all_answers, \
    get_random_users

app = get_app() #  Explicitando uma variável app nesse arquivo para o Heroku achar


@app.route('/sitemap.xml', methods=['GET'])
def sitemap():
    response = make_response(open('%s/bands/static/sitemap.xml' % project_root).read())
    response.headers["Content-type"] = "text/plain"
    return response


@app.route('/robots.txt', methods=['GET'])
def robots():
    response = make_response(open('%s/bands/static/robots.txt' % project_root).read())
    response.headers["Content-type"] = "text/plain"
    return response


@app.route('/google3d434de8eb17df82.html')
def google_webmaster():
    return render_template("google_web_master.html")


@app.route('/resultados-gerais/<password>/', methods=['GET'])
@need_to_be_admin
def resultados(password):
    current_user = session['current_user']

    password_compare = os.environ["PASSWORD_RESULTS"] if os.environ.has_key("PASSWORD_RESULTS") else "kyb@1234"
    if password == password_compare:
        questions_and_all_answers = get_all_questions_and_all_answers()
        return render_template('resultados_gerais.html', current_user=current_user,
                                questions_and_all_answers=questions_and_all_answers)
    else:
        abort(404)

@app.route('/')
def index():
    users_random, total_users = get_random_users()
    return render_template("index.html", users=users_random, total_users=total_users)


@app.route('/pesquisa-sucesso/', methods=['GET'])
@need_to_be_logged
def pesquisa_sucesso():
    current_user = session['current_user']

    return render_template('pesquisa_success.html', current_user=current_user)


@app.route('/pesquisa/', methods=['GET', 'POST'])
@need_to_be_logged
def pesquisa():
    current_user = session['current_user']

    post_data = prepare_post_data()

    if request.method == 'POST':
        if validate_answers(post_data):
            save_answers(post_data, current_user)
            return redirect(url_for('pesquisa_sucesso'))


    return render_template('pesquisa.html', current_user=current_user, main_questions=MAIN_QUESTIONS,
                            questions=QUESTIONS_PESQUISA, post_data=post_data)


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
