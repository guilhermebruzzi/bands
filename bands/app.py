#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import urllib2
import json

from flask import Flask, redirect, url_for, session, request, abort, make_response
from config import get_app, facebook, MAIN_QUESTIONS, QUESTIONS_PESQUISA, project_root
from helpers import prepare_post_data, need_to_be_logged, need_to_be_admin, get_current_user, \
    get_slug, render_template, get_client_ip, get_current_city
from controllers import get_or_create_user, validate_answers, save_answers, get_all_questions_and_all_answers, \
    get_random_users, random_top_bands, get_user_bands, get_or_create_band, like_band, unlike_band, get_top_bands, \
    get_all_users, get_related_bands, get_band, get_user_answers, get_answers_and_counters_from_question, \
    get_shows_from_bands, get_shows_from_bands_by_city

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
        users = get_all_users()
        top_bands, len_bands = get_top_bands(sort=True)
        funcionalidades_fa = get_answers_and_counters_from_question(['fa-funcionalidades'])
        funcionalidades_musico = get_answers_and_counters_from_question(['musico-funcionalidades'])
        return render_template('resultados_gerais.html', current_user=current_user,
                                questions_and_all_answers=questions_and_all_answers.values(),
                                users=users, funcionalidades_fa=funcionalidades_fa,funcionalidades_musico=funcionalidades_musico,
                                bands=top_bands, len_bands=len_bands)
    else:
        abort(404)

@app.route('/', methods=['GET'])
def index():
    users_random, total_users = get_random_users()
    current_user = get_current_user()

    max = 15
    sort = True
    normalize = False

    bands, total = get_top_bands(max=max, sort=sort, normalize=normalize)
    bands_objects = [band["band_object"] for band in bands]
    shows = get_shows_from_bands(bands_objects, 1)
    current_city = get_current_city(ip=get_client_ip())
    shows_locais = get_shows_from_bands_by_city(city=current_city)

    return render_template("index.html", users=users_random, total_users=total_users, bands=bands,
        current_user=current_user, total=total, shows=shows, shows_locais=shows_locais)


@app.route('/minhas-bandas/', methods=['GET'])
@need_to_be_logged
def minhas_bandas():
    current_user = get_current_user()
    bands = random_top_bands(user=current_user)
    bands_user = get_user_bands(user=current_user)
    thanks_msg = "Obrigado por responder a pesquisa!" if request.referrer and url_for("pesquisa") in request.referrer else ""

    return render_template('minhas_bandas.html', current_user=current_user, bands=bands, bands_user=bands_user,
                            thanks_msg=thanks_msg)


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


@app.route('/band/related_bands/<slug>/', methods=['GET'])
@need_to_be_logged
def related_bands(slug):
    related_bands = get_related_bands(get_band(slug), max=10, user=get_current_user())
    result = ""

    for slug in related_bands:
        result += slug + "\n"
        result += get_band(slug).name + "\n"

    return result


@app.route('/pesquisa/', methods=['GET', 'POST'])
@need_to_be_logged
def pesquisa():
    current_user = get_current_user()
    post_data = prepare_post_data()

    if request.method == 'POST':
        if validate_answers(post_data):
            save_answers(post_data, current_user)
            return redirect(url_for('minhas_bandas'))

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

    user_answers = get_user_answers(session['current_user']) #  if no answers given, go to feedback form
    url = url_for('pesquisa') if len(user_answers) == 0 else url_for('minhas_bandas')
    return redirect(url)


@facebook.tokengetter
def get_facebook_oauth_token():
    return session.get('oauth_token')


if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
