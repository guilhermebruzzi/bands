#!/usr/bin/env python
#-*- coding:utf-8 -*-

import flask
from unittest import TestCase
from helpers import get_slug, user_logged, need_to_be_logged, count_tags
from config import get_app
from models import User
from app import app

class HelpersTest(TestCase):

    def setUp(self):
        self.app = app # Iguala ao flask completo

        self.guilherme_user = User(facebook_id="100000002085352", email="guibruzzi@gmail.com", name="Guilherme Heynemann Bruzzi")

        self.title_normal = "Whos Using It?"
        self.title_unicode = u"Este é um outro teste éÃÂ"

        self.tags = {
            "Foo Fighters": 60,
            "The Beatles": 50,
            "The Who": 40,
            "Chico Buarque": 30,
            "Madonna": 20,
            "Los Hermanos": 5,
        }


    def get_slug_test(self):
        slug = get_slug(self.title_normal)
        self.assertEqual(slug, "whos-using-it")


    def get_slug_with_unicode_test(self):
        slug = get_slug(self.title_unicode)
        self.assertEqual(slug, "este-e-um-outro-teste-eaa")


    def user_logged_test(self):
        with self.app.test_request_context():
            self.assertFalse(user_logged())
            flask.session['current_user'] = self.guilherme_user
            self.assertTrue(user_logged())

    def __get_tag_index__(self, tagclouds, label):
        for index in range(len(tagclouds)):
            if tagclouds[index]["label"] == label:
                return index
        return None

    def count_tags_test(self):
        tagclouds = count_tags(self.tags)
        self.assertEqual(len(tagclouds), 6)

        index = self.__get_tag_index__(tagclouds, "Foo Fighters")
        self.assertNotEqual(index, None)
        self.assertEqual(tagclouds[index]["size"], 6)

        index = self.__get_tag_index__(tagclouds, "Chico Buarque")
        self.assertNotEqual(index, None)
        self.assertEqual(tagclouds[index]["size"], 3)

        index = self.__get_tag_index__(tagclouds, "Los Hermanos")
        self.assertNotEqual(index, None)
        self.assertEqual(tagclouds[index]["size"], 0)


    def need_to_be_logged_test(self):
        pass
#        with app.test_client() as client:
#            with client.session_transaction() as sess:
#
#                self.__need_to_be_logged_helper__ = need_to_be_logged(self.__need_to_be_logged_helper__)
#                self.app.add_url_rule('/need_to_be_logged/', '__need_to_be_logged_helper__', self.__need_to_be_logged_helper__)
#
#                response_not_logged = client.get("/need_to_be_logged/", follow_redirects=True)
#                self.assertIn("Bands", response_not_logged.data)
#
#                sess['current_user'] = self.guilherme_user
#
#                response_logged = client.get("/need_to_be_logged/", follow_redirects=True)
#                self.assertIn("logged", response_logged.data)


    def __need_to_be_logged_helper__(self):
        return "logged"
