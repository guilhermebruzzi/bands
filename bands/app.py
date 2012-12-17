#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import urllib2
import json

from flask import Flask, redirect, url_for, session, request, abort, make_response
from config import get_app, facebook, MAIN_QUESTIONS, QUESTIONS_PESQUISA, TAGS, project_root
from helpers import prepare_post_data, need_to_be_logged, need_to_be_admin, count_tags, get_current_user, \
    get_musicians_from_opengraph, get_slug, render_template
from controllers import get_or_create_user, validate_answers, save_answers, get_all_questions_and_all_answers, \
    get_random_users, random_top_bands, get_user_bands, get_or_create_band, like_band, unlike_band, get_top_bands

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
    current_user = get_current_user()

    password_compare = os.environ["PASSWORD_RESULTS"] if os.environ.has_key("PASSWORD_RESULTS") else "kyb@1234"
    if password == password_compare:
        questions_and_all_answers = get_all_questions_and_all_answers()
        return render_template('resultados_gerais.html', current_user=current_user,
                                questions_and_all_answers=questions_and_all_answers)
    else:
        abort(404)

@app.route('/', methods=['GET'])
def index():
    mode = request.args.get('mode')
    users_random, total_users = get_random_users()
    current_user = get_current_user()

    max = 15
    sort = True

    if mode != "bandslist":
        mode = "tagcloud"
        max = 40
        sort = False

    bands, total = get_top_bands(max, sort)

    return render_template("index.html", users=users_random, total_users=total_users, bands=bands,
        current_user=current_user, mode=mode, total=total)


@app.route('/pesquisa-sucesso/', methods=['GET'])
@need_to_be_logged
def pesquisa_sucesso():
    current_user = get_current_user()
    bands = random_top_bands(user=current_user)
    bands_user = get_user_bands(user=current_user)

    return render_template('pesquisa_success.html', current_user=current_user, bands=bands, bands_user=bands_user)


@app.route('/band/add/', methods=['POST'])
@need_to_be_logged
def add_band():
    name = request.form['band']
    user = get_current_user()

    band = get_or_create_band({'slug': get_slug(name), 'name': name, 'user': user})
    return "%s\n%s" % (band.name, band.slug)


@app.route('/band/like/', methods=['POST'])
@need_to_be_logged
def like():
    slug = request.form['band']
    user = get_current_user()

    like_band(slug, user)
    return 'liked'


@app.route('/band/unlike/', methods=['POST'])
@need_to_be_logged
def unlike():
    slug = request.form['band']
    user = get_current_user()

    unlike_band(slug, user)
    return 'unliked'


@app.route('/pesquisa/', methods=['GET', 'POST'])
@need_to_be_logged
def pesquisa():
    current_user = get_current_user()
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

@app.route('/logout/')
@need_to_be_logged
def logout():
    del session['current_user']
    return redirect(url_for('index'))

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
    session['current_user'] = get_or_create_user(me.data, oauth_token=resp['access_token'])

    return redirect(url_for('pesquisa'))


@facebook.tokengetter
def get_facebook_oauth_token():
    return session.get('oauth_token')


if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
