#!/usr/bin/env python
#-*- coding:utf-8 -*-

import flask
from unittest import TestCase
from facebook import *
from app import app

class FacebookTest(TestCase):

    def setUp(self):
        self.app = app # Iguala ao flask completo
        self.guilherme_bruzzi_facebook_id = "100000002085352"
        self.perfil_teste_facebook_id = "100003570444698"
        self.access_token = 'AAAEGO5mvMs0BAKSs368jVzpVIMeKspas62h6zyaALAdMbXF1T5qYCFxboPJA5MRyo9tqPZCWggM8oQ3IfhkPyeoZAxWDV9DnxAygqxTQZDZD'

    def get_musicians_from_opengraph_test(self):
        musicians = get_musicians_from_opengraph(self.guilherme_bruzzi_facebook_id, self.access_token)
        self.assertEqual(type(musicians), list)
        self.assertIn("Foo Fighters", musicians)

    def get_facebook_data_test(self):
        facebook_data = get_facebook_data(self.access_token)
        self.assertNotEqual(facebook_data['id'], self.perfil_teste_facebook_id)
        self.assertEqual(facebook_data['id'], self.guilherme_bruzzi_facebook_id, msg=u"Esse access token se refere ao perfil guilherme")
