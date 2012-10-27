# -*- coding: utf-8 -*-

import os

from flask import Flask
from flaskext.oauth import OAuth
from flaskext.mongoengine import MongoEngine

app = Flask(__name__)
app.config.from_pyfile('app.cfg')

for key in app.config.keys():
    if os.environ.has_key(key):
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

QUESTIONS_PESQUISA = [
    {
        "class_name": "musico",
        "type": "checkbox_textarea",
        "question": u"Quais as suas bandas (ou músicos) favoritas?",
        "answers": sorted([ u"The Beatles",  u"Foo Fighters", u"Los Hermanos", u"Chico Buarque", u"Madonna"]),
        "outros": u"A lista acima contém as mais faladas aqui no site, digite outras que você gosta:"
    },
    {
        "class_name": "musico",
        "type": "checkbox_textarea",
        "question": u"Quais dificuldades você enfrenta na sua banda?",
        "answers": [ u"Divulgar os shows",  u"Divulgar as minhas músicas e clipes",
                     u"Vender os ingressos dos meus shows e eventos",
                     u"Vender os produtos da minha banda (álbuns, camisas, etc.)" ],
        "outros": u"Nos diga quaisquer outras dificuldades:"
    },
    {
        "class_name": "musico",
        "type": "textarea",
        "question": u"Atualmente, como você resolve os problemas que marcou acima?"
    },
    {
        "class_name": "musico",
        "type": "checkbox_textarea",
        "question": u"Quais as funcionalidades mais importantes que você gostaria que tivesse no site?",
        "answers": [ u"Venda de ingressos",  u"Merchandising (roupas, acessórios, etc)", u"Histórico da banda",
                     u"Divulgação de shows e eventos", u"Lista de Integrantes das bandas (atuais e ex-integrantes)",
                     u"Links para redes sociais e site oficial das bandas e músicos",
                     u"Vídeos das bandas e músicos (shows e clipes)", u"Discografia das bandas e músicos",
                     u"Fãs podendo dar nota (pra banda, pro cd, pro show)",
                     u"Fãs podendo dar resenhas (pra banda, pro cd, pro show)" ],
        "outros": u"Nos diga quaisquer outras funcionalidades que acharia interessante ter no site:"
    },
    {
        "class_name": "musico",
        "type": "checkbox_textarea",
        "question": u"Que nome para esse produto você gosta mais?",
        "answers": [ u"Bands", u"Bands.Info", u"Know Your Band", u"Bandpedia", u"Musicopedia", ],
        "outros": u"Dê outro(s) nome(s) que acharia interessante:"
    },
    {
        "class_name": "fa",
        "type": "checkbox_textarea",
        "question": u"Quais as suas bandas (ou músicos) favoritas?",
        "answers": sorted([ u"The Beatles",  u"Foo Fighters", u"Los Hermanos", u"Chico Buarque", u"Madonna"]),
        "outros": u"A lista acima contém as mais faladas aqui no site, digite outras que você gosta:"
    },
    {
        "class_name": "fa",
        "type": "checkbox_textarea",
        "question": u"Quais as funcionalidades mais importantes que você gostaria que tivesse no site?",
        "answers": [ u"Venda de ingressos",  u"Merchandising (roupas, acessórios, etc)", u"Histórico da banda",
                     u"Divulgação de shows e eventos", u"Lista de Integrantes das bandas (atuais e ex-integrantes)",
                     u"Links para redes sociais e site oficial das bandas e músicos",
                     u"Vídeos das bandas e músicos (shows e clipes)", u"Discografia das bandas e músicos",
                     u"Fãs podendo dar nota (pra banda, pro cd, pro show)",
                     u"Fãs podendo dar resenhas (pra banda, pro cd, pro show)" ],
        "outros": u"Nos diga quaisquer outras funcionalidades que acharia interessante ter no site:"
    },
    {
        "class_name": "fa",
        "type": "checkbox_textarea",
        "question": u"Que nome para esse produto você gosta mais?",
        "answers": [ u"Bands", u"Bands.Info", u"Know Your Band", u"Bandpedia", u"Musicopedia", ],
        "outros": u"Dê outro(s) nome(s) que acharia interessante:"
    },
]
