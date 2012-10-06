#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
from flask import Flask, redirect, url_for, session, request, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/pesquisa-usabilidade/<login>/<int:idade>')
def pesquisa(login, idade):
    return render_template("pesquisa.html", login=login, idade=idade)

def run():
    app.run()

if __name__ == '__main__':
    run()
