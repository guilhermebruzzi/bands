# -*- coding: utf-8 -*-

import os
import sys

from flask import Flask
from flask_oauth import OAuth
from flaskext.mongoengine import MongoEngine
from flask.ext import assets
from flask.ext.jasmine import Jasmine
from flask.ext.cache import Cache

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

jasmine = Jasmine(app)

jasmine.specs(
    'js/jquery-1.9.1.min.js',
    'js/jasmine/fixtures/venda-produtos-fixture.js',
    'js/jasmine/specs/venda-produtos-spec.js',
    'js/jasmine/fixtures/index-btn-fixture.js',
    'js/jasmine/specs/index-btn-spec.js',
    'js/jasmine/fixtures/novo-fixture.js',
    'js/jasmine/specs/novo-spec.js',
)

jasmine.sources(
    'js/base.js',
    'js/venda-produtos.js',
    'js/index.js',
)

cache = Cache(app)

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
        "slug": "musico-dificuldades",
        "class_name": "musico",
        "type": "checkbox_textarea",
        "question": u"Quais dificuldades você enfrenta na sua banda?",
        "answers": [ u"Divulgar os shows",  u"Divulgar as minhas músicas e clipes",
                     u"Vender os ingressos dos meus shows e eventos",
                     u"Vender os produtos da minha banda (álbuns, camisas, etc.)" ],
        "outros": u"Nos diga quaisquer outras dificuldades:"
    }
]

BANDAS_CAMISAS = {
    "coldplay" : {
        "nome": "Coldplay",
        "slug": "coldplay",
        "camisas": [
            { "tipo": "viva la vida", "preco": "20,00" },
        ]
    },
    "guns-n-roses": {
        "nome": "Guns n' Roses",
        "slug": "guns-n-roses",
        "camisas": [
            { "tipo": "caveira", "preco": "22,00" },
        ]
    },
    "los-bife": {
        "nome": "Los Bife",
        "slug": "los-bife",
        "camisas": [
            { "tipo": "amarela", "preco": "35,00" },
            { "tipo": "vermelha", "preco": "35,00" },
            { "tipo": "azul", "preco": "35,00" },
            { "tipo": "verde", "preco": "35,00" },
        ]
    },
    "los-hermanos": {
        "nome": "Los Hermanos",
        "slug": "los-hermanos",
        "camisas": [
            { "tipo": "sentimental", "preco": "22,00" },
        ]
    },
    "metallica": {
        "nome": "Metallica",
        "slug": "metallica",
        "camisas": [
            { "tipo": "branca", "preco": "19,00" },
            { "tipo": "james hetfield", "preco": "22,00" }
        ]
    },
    "queen": {
        "nome": "Queen",
        "slug": "queen",
        "camisas": [
            { "tipo": "preta", "preco": "22,00" },
        ]
    },
    "the-beatles": {
        "nome": "The Beatles",
        "slug": "the-beatles",
        "camisas": [
            { "tipo": "integrantes", "preco": "23,00" },
        ]
    },
    "tim-maia": {
        "nome": "Tim Maia",
        "slug": "tim-maia",
        "camisas": [
            { "tipo": "preta", "preco": "33,00" },
        ]
    }
}

BANDAS_CAMISAS_HOME = [BANDAS_CAMISAS["guns-n-roses"], BANDAS_CAMISAS["los-hermanos"], BANDAS_CAMISAS["metallica"], BANDAS_CAMISAS["tim-maia"]]

def get_app():
    return app
