# -*- coding: utf-8 -*-

import os
import sys

from flask import Flask
from flaskext.oauth import OAuth
from flaskext.mongoengine import MongoEngine
from flask.ext import assets

def add_path():
    global project_root
    file_path = os.path.abspath(os.path.dirname(__file__))
    project_root = os.path.abspath("%s/../" % file_path)
    sys.path.insert(0, project_root)
    return project_root

project_root = add_path()

def import_folder(folder_name, base_path = None):
    full_path = os.path.join(base_path, folder_name)
    folder = os.path.abspath(full_path)
    sys.path.insert(0, folder)


import_folder(folder_name='bands', base_path=project_root)

app = Flask(__name__)
app.config.from_pyfile('app.cfg')

for key in app.config.keys():
    if os.environ.has_key(key):
        type_of_config = type(app.config[key])
        if type_of_config is bool:
            if os.environ[key] == "False":
                app.config[key] = False
            else:
                app.config[key] = True
        elif type_of_config is int:
            app.config[key] = int(os.environ[key])
        else:
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
assets = assets.Environment()
assets.init_app(app)

MAIN_QUESTIONS = [
    {
        "slug": "musico-ou-fa",
        "class_name": "answer_main",
        "type": "radio",
        "question": u"Você é músico?",
        "answers": [ { "value": u"musico", "label": u"Sim" }, { "value": u"fa", "label": u"Não" } ]
    },
]

QUESTIONS_PESQUISA = [
    {
        "slug": "musico-favoritos",
        "class_name": "musico",
        "type": "checkbox_textarea",
        "question": u"Quais as suas bandas ou músicos favoritos?",
        "answers": sorted([ u"The Beatles",  u"Foo Fighters", u"Los Hermanos", u"Chico Buarque", u"Madonna"]),
        "outros": u"A lista acima contém as mais faladas aqui no site, digite outras que você gosta:"
    },
    {
        "slug": "musico-dificuldades",
        "class_name": "musico",
        "type": "checkbox_textarea",
        "question": u"Quais dificuldades você enfrenta na sua banda?",
        "answers": [ u"Divulgar os shows",  u"Divulgar as minhas músicas e clipes",
                     u"Vender os ingressos dos meus shows e eventos",
                     u"Vender os produtos da minha banda (álbuns, camisas, etc.)" ],
        "outros": u"Nos diga quaisquer outras dificuldades:"
    },
    {
        "slug": "musico-solucao",
        "class_name": "musico",
        "type": "textarea",
        "question": u"Atualmente, como você resolve os problemas que marcou acima?"
    },
    {
        "slug": "musico-funcionalidades",
        "class_name": "musico",
        "type": "checkbox_textarea",
        "question": u"Quais as funcionalidades mais importantes que você gostaria que tivesse no site?",
        "answers": [ u"Venda de ingressos",  u"Merchandising (cds, roupas, acessórios, etc)", u"Histórico da banda",
                     u"Divulgação de shows e eventos", u"Lista de Integrantes das bandas (atuais e ex-integrantes)",
                     u"Links para redes sociais e site oficial das bandas e músicos",
                     u"Vídeos das bandas e músicos (shows e clipes)", u"Músicas das bandas e músicos",
                     u"Fãs podendo dar nota (pra banda, pro cd, pro show)",
                     u"Fãs podendo dar resenhas (pra banda, pro cd, pro show)" ],
        "outros": u"Nos diga quaisquer outras funcionalidades que acharia interessante ter no site:"
    },
    {
        "slug": "musico-nome",
        "class_name": "musico",
        "type": "checkbox_textarea",
        "question": u"Que nome para esse produto você gosta mais?",
        "answers": [ u"Bands", u"Bands.Info", u"Know Your Band", u"Bandpedia", u"Musicopedia", ],
        "outros": u"Dê outro(s) nome(s) que acharia interessante:"
    },
    {
        "slug": "fa-favoritos",
        "class_name": "fa",
        "type": "checkbox_textarea",
        "question": u"Quais as suas bandas ou músicos favoritos?",
        "answers": sorted([ u"The Beatles",  u"Foo Fighters", u"Los Hermanos", u"Chico Buarque", u"Madonna"]),
        "outros": u"A lista acima contém as mais faladas aqui no site, digite outras que você gosta:"
    },
    {
        "slug": "fa-funcionalidades",
        "class_name": "fa",
        "type": "checkbox_textarea",
        "question": u"Quais as funcionalidades mais importantes que você gostaria que tivesse no site?",
        "answers": [ u"Venda de ingressos",  u"Merchandising (cds, roupas, acessórios, etc)", u"Histórico da banda",
                     u"Divulgação de shows e eventos", u"Lista de Integrantes das bandas (atuais e ex-integrantes)",
                     u"Links para redes sociais e site oficial das bandas e músicos",
                     u"Vídeos das bandas e músicos (shows e clipes)", u"Músicas das bandas e músicos",
                     u"Fãs podendo dar nota (pra banda, pro cd, pro show)",
                     u"Fãs podendo dar reviews (pra banda, pro cd, pro show)" ],
        "outros": u"Nos diga quaisquer outras funcionalidades que acharia interessante ter no site:"
    },
    {
        "slug": "fa-nome",
        "class_name": "fa",
        "type": "checkbox_textarea",
        "question": u"Que nome para esse produto você gosta mais?",
        "answers": [ u"Bands", u"Bands.Info", u"Know Your Band", u"Bandpedia", u"Musicopedia", ],
        "outros": u"Dê outro(s) nome(s) que acharia interessante:"
    },
]

TAGS = {
    u"Chico Buarque": 12,
    u"Madonna": 2,
    u"Foo Fighters": 4,
    u"Los Hermanos": 6,
    u"The Beatles": 7,
    u"Led Zeppelin": 1,
    u"Paralamas": 1,
    u"Arctic Monkeys": 3,
    u"Franz Ferdinand": 1,
    u"Linkin Park": 1,
    u"The Who": 1,
    u"Keane": 1,
    u"Coldplay": 1,
    u"The Killers": 1,
    u"The Strokes": 2,
    u"Móveis Coloniais de Acaju": 1,
    u"A banda mais bonita da cidade": 1,
    u"Léo Fressato": 1,
    u"Mohandas": 1,
    u"Adele": 1,
    u"Amy Winehouse": 2,
    u"Cazuza": 1,
    u"Cícero": 1,
    u"Lulu Santos": 1,
    u"Frank Sinatra": 1,
    u"Tom Jobim": 1,
    u"Marisa Monte": 1,
    u"Adriana Calcanhoto": 1,
    u"Jonis": 1,
    u"Jimmy Hendrix": 1,
    u"Whitney Houston": 1,
    u"Rolling Stones": 2,
    u"Elis Regina": 1,
    u"Gal Costa": 1,
    u"Charles Aznavour": 1,
    u"Cartola": 1,
    u"Michael Bublé": 1,
    u"Tracy Chapman": 1,
    u"Adele": 1,
    u"Seu Jorge": 1,
    u"Maria Gadu": 1,
    u"Tiago Iorc": 1,
    u"Roberta Sá": 1,
    u"Robin Thicke": 1,
    u"The Clash": 1,
    u"Kinks": 1,
    "Rolling Stones": 1,
    u"Los Bife": 1,
    u"The Smiths": 1,
    u"U2": 2,
    u"Ganeshas": 1,
    u"The Cribs": 1,
    u"Spiritualized": 1,
    u"The Alan Parsons Project": 1,
    u"Guns N' Roses": 1,
    u"Ratto": 1,
    u"CPM22": 1,
    u"Green Day": 1,
    u"Gun's and Roses": 1,
}

def get_app():
    return app
