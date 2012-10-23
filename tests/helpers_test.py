#!/usr/bin/env python
#-*- coding:utf-8 -*-

from unittest import TestCase
from helpers import get_slug, user_logged
from models import User

class HelpersTest(TestCase):

    def setUp(self):
        self.title_normal = "Whos Using It?"
        self.title_unicode = u"Este é um outro teste éÃÂ"

    def get_slug_test(self):
        slug = get_slug(self.title_normal)
        self.assertEqual(slug, "whos-using-it")

    def get_slug_with_unicode_test(self):
        slug = get_slug(self.title_unicode)
        self.assertEqual(slug, "este-e-um-outro-teste-eaa")

    def user_logged_test(self):
        session = {}
        self.assertFalse(user_logged(session))
        session['current_user'] = User(facebook_id="guto", email="guto@marzagao.com", name="Guto Marzagao")
        self.assertTrue(user_logged(session))
        del session['current_user']

