#!/usr/bin/python
# -*- coding: utf-8 -*-

import os

from models import *
from flask import Flask, redirect, url_for, session, request, abort, make_response
from config import get_app, facebook, MAIN_QUESTIONS, project_root, BANDAS_CAMISAS, BANDAS_CAMISAS_HOME
from helpers import need_to_be_logged, need_to_be_admin, get_current_user, get_slug, render_template, get_client_ip, \
    has_cookie_login, set_cookie_login, delete_cookie_login, user_logged, make_login, get_cookie_login
from controllers import get_or_create_user, validate_answers, random_top_bands, get_user_bands, \
    get_or_create_band, like_band, unlike_band, get_top_bands, get_all_users, get_related_bands, get_band, \
    get_answers_and_counters_from_question, get_shows_from_bands, get_shows_from_bands_by_city, set_user_tipo,\
    newsletter_exists, get_or_create_newsletter, get_all_bands, get_all_newsletters
from pagseguropy.pagseguro import Pagseguro


app = get_app() #  Explicitando uma variável app nesse arquivo para o Heroku achar

def __make_response_plain_text__(response_text):
    response = make_response(response_text)
    response.headers["Content-type"] = "text/plain"
    return response

@app.route('/sitemap.xml', methods=['GET'])
def sitemap():
    return __make_response_plain_text__(open('%s/bands/static/sitemap.xml' % project_root).read())


@app.route('/robots.txt', methods=['GET'])
def robots():
    return __make_response_plain_text__(open('%s/bands/static/robots.txt' % project_root).read())


@app.route('/google3d434de8eb17df82.html')
def google_webmaster():
    return render_template("google_web_master.html")


@app.route('/resultados-gerais/<password>/', methods=['GET'])
@need_to_be_admin
def resultados(password):
    current_user = get_current_user()

    password_compare = os.environ["PASSWORD_RESULTS"] if os.environ.has_key("PASSWORD_RESULTS") else "kyb@1234"
    if password == password_compare:
        users = get_all_users()
        top_bands, len_bands = get_top_bands(sort=True)
        funcionalidades_fa = get_answers_and_counters_from_question(['fa-funcionalidades'])
        funcionalidades_musico = get_answers_and_counters_from_question(['musico-funcionalidades'])

        newsletters = get_all_newsletters()

        return render_template('resultados_gerais.html', current_user=current_user, users=users,
            funcionalidades_fa=funcionalidades_fa, funcionalidades_musico=funcionalidades_musico,
            bands=top_bands, len_bands=len_bands, newsletters=newsletters)
    else:
        abort(404)
@app.route('/', methods=['GET'])
def index():
    if has_cookie_login(request) and not user_logged():
        make_login(oauth_token=get_cookie_login(request))

    current_user = get_current_user()
    current_city = current_user.city if current_user and current_user.city else "Rio de Janeiro"

    minhas_bandas_shows = []
    if current_user:
        minhas_bandas = get_user_bands(user=current_user)
        minhas_bandas_shows = get_shows_from_bands(minhas_bandas, 1, city=current_city)

    shows_locais = get_shows_from_bands_by_city(city=current_city)

    newsletter = newsletter_exists(tipo="Shows", user=current_user)

    all_bands = get_all_bands()
    top_bands = get_top_bands(max=3, maxSize=10)[0]
    top_shows = get_shows_from_bands([band["band_object"] for band in top_bands], 1, city=current_city)

    carrinho = Pagseguro(email_cobranca="guibruzzi@gmail.com", tipo='CP', frete=10.0) # CP é para poder usar o método cliente
    formulario_pag_seguro = carrinho.mostra(imprime=False, imgBotao="/static/img/pagseguro.png")

    return render_template("index.html", current_user=current_user, minhas_bandas_shows=minhas_bandas_shows,
        shows_locais=shows_locais, newsletter=newsletter, all_bands=all_bands, top_shows=top_shows, current_city=current_city,
        BANDAS_CAMISAS_HOME=BANDAS_CAMISAS_HOME, formulario_pag_seguro=formulario_pag_seguro)

@app.route('/novo/', methods=['GET'])
def novo():
    if has_cookie_login(request) and not user_logged():
        make_login(oauth_token=get_cookie_login(request))

    current_user = get_current_user()
    current_city = current_user.city if current_user and current_user.city else "Rio de Janeiro"

    minhas_bandas_shows = []
    if current_user:
        minhas_bandas = get_user_bands(user=current_user)
        minhas_bandas_shows = get_shows_from_bands(minhas_bandas, 1, city=current_city)

    all_bands = get_all_bands()
    top_bands = get_top_bands(max=3, maxSize=10)[0]
    top_shows = get_shows_from_bands([band["band_object"] for band in top_bands], 1, city=current_city)
    minhas_bandas_shows.extend(top_shows)

    shows_locais = get_shows_from_bands_by_city(city=current_city)
    for show_local in shows_locais:
        main_artist = show_local.artists[0]
        minhas_bandas_shows.append((main_artist, [show_local]))

    return render_template("novo.html", current_user=current_user,
        minhas_bandas_shows=minhas_bandas_shows, all_bands=all_bands)


@app.route('/loja-virtual', methods=['GET'])
def loja_virtual():
    carrinho = Pagseguro(email_cobranca="guibruzzi@gmail.com", tipo='CP', frete=10.0) # CP é para poder usar o método cliente
    current_user = get_current_user()

    formulario_pag_seguro = carrinho.mostra(imprime=False, imgBotao="/static/img/pagseguro.png")
    produtos_section = True if request.args.get('produtos-section') else False
    dark = True if request.args.get('dark') else False

    return render_template('loja_virtual.html', current_user=current_user, formulario_pag_seguro=formulario_pag_seguro,
        range_quantidade=range(2, 10), range_tamanhos=['pp', 'p', 'm', 'g'], produtos_section=produtos_section, dark=dark,
        camisas=BANDAS_CAMISAS)

@app.route('/newsletter/<option>', methods=['POST'])
def salvar_newsletter(option):
    user_id = request.form['user_id']
    current_user = get_or_create_user({"id": user_id})
    tipo = request.form['tipo']
    option = option == "sim"
    newsletter_answer = unicode(get_or_create_newsletter(option=option, user=current_user, tipo=tipo))
    return __make_response_plain_text__(newsletter_answer)

@app.route('/show_from_band/<band_name>', methods=['GET', 'POST'])
def show_from_band(band_name):
    current_user = None # TODO: Adicionar em minhas bandas: get_current_user()
    current_city = "Rio de Janeiro" # get_current_city(ip=get_client_ip())
    band = get_or_create_band({'slug': get_slug(band_name), 'name': band_name, 'user': current_user})
    shows = get_shows_from_bands([band], limit_per_artist=1, city=current_city, call_lastfm_if_dont_have_shows=True, call_lastfm_without_subprocess=True)
    show = None
    if shows:
        show = shows[0][1][0] # Pegando apenas o objeto show da banda
    return render_template("show_de_uma_banda.html", band=band, show=show)

@app.route('/search_band/<band_name>', methods=['GET', 'POST'])
def search_band(band_name):
    current_user = None # TODO: Adicionar em minhas bandas: get_current_user()
    current_city = "Rio de Janeiro" # get_current_city(ip=get_client_ip())
    band = get_or_create_band({'slug': get_slug(band_name), 'name': band_name, 'user': current_user})
    shows = get_shows_from_bands([band], limit_per_artist=1, city=current_city, call_lastfm_if_dont_have_shows=True, call_lastfm_without_subprocess=True)
    show = None
    if shows:
        show = shows[0][1][0] # Pegando apenas o objeto show da banda
    return render_template("resultado_uma_banda.html", band=band, show=show)

@app.route('/minhas-bandas/', methods=['GET'])
@need_to_be_logged
def minhas_bandas():
    current_user = get_current_user()
    bands = random_top_bands(user=current_user)
    bands_user = get_user_bands(user=current_user)

    resp = make_response(render_template('minhas_bandas.html', current_user=current_user, bands=bands, bands_user=bands_user))
    set_cookie_login(resp, oauth_token=get_facebook_oauth_token()[0])
    return resp

@app.route('/los-bife', methods=['GET'])
def los_bife():
    carrinho = Pagseguro(email_cobranca="guibruzzi@gmail.com", tipo='CP', frete=10.0) # CP é para poder usar o método cliente
    carrinho.item(id=1, descr='CD Los Bife', qty=0, valor=15.0)
    carrinho.item(id=2, descr='Camisa Los Bife', qty=0, valor=20.0)
    current_user = get_current_user()

    formulario_pag_seguro = carrinho.mostra(imprime=False, imgBotao="/static/img/pagseguro.png")
    produtos_section = True if request.args.get('produtos-section') else False
    dark = True if request.args.get('dark') else False
    return render_template('venda_los_bife.html', current_user=current_user, formulario_pag_seguro=formulario_pag_seguro,
        range_quantidade=range(2, 10), range_tamanhos=['pp', 'p', 'm', 'g'], produtos_section=produtos_section, dark=dark,
        camisas=[{ "tipo": "amarela", "preco": "20,00" },
                 { "tipo": "vermelha", "preco": "20,00" }])

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


@app.route('/cadastro/', methods=['GET', 'POST'])
@need_to_be_logged
def cadastro():
    current_user = get_current_user()
    data = request.form

    if request.method == 'POST':
        if validate_answers(data):
            set_user_tipo(current_user, data["musico-ou-fa"])

            if data["banda"]:
                get_or_create_band({"name": data["banda"], "musician": current_user})

            return redirect(url_for('minhas_bandas'))

    return render_template('cadastro.html', current_user=current_user, main_questions=MAIN_QUESTIONS, post_data=data)


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
    resp = redirect(url_for('index'))
    if has_cookie_login(request):
        delete_cookie_login(resp)
    return resp

@app.route('/login/authorized/')
@facebook.authorized_handler
def facebook_authorized(resp):
    if resp is None:
        return 'Access denied: reason=%s error=%s' % (
            request.args['error_reason'],
            request.args['error_description']
        )

    make_login(oauth_token=resp['access_token'])

    next_url = url_for('minhas_bandas') if session['current_user'].tipo else url_for('cadastro')
    return redirect(next_url)


@facebook.tokengetter
def get_facebook_oauth_token():
    return session.get('oauth_token')


if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
