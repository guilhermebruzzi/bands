#!/usr/bin/env python
#-*- coding:utf-8 -*-

from unittest import TestCase
from helpers import get_slug, get_or_create_user
from models import User

class HelpersTest(TestCase):

    def setUp(self):
        self.title_normal = "Whos Using It?"
        self.title_unicode = u"Este é um outro teste éÃÂ"
        self.data_user_guilherme = {"id": "bands2012", "email":"guibruzzi@gmail.com", "name":"Guilherme"}
        self.data_user_guto = {"id": "bands2013", "email":"gutomarzagao@gmail.com", "name":"Guto Marra"}
        for user in User.objects:
            user.delete()

    def tearDown(self):
        for user in User.objects:
            user.delete()

    def get_slug_test(self):
        slug = get_slug(self.title_normal)
        self.assertEqual(slug, "whos-using-it")

    def get_slug_with_unicode_test(self):
        slug = get_slug(self.title_unicode)
        self.assertEqual(slug, "este-e-um-outro-teste-eaa")

    def get_or_create_user_maintain_object_test(self):
        user_guilherme = get_or_create_user(data=self.data_user_guilherme)
        self.assertEqual(user_guilherme.facebook_id, self.data_user_guilherme["id"])

        user_guilherme = get_or_create_user(data=self.data_user_guilherme)
        self.assertEqual(user_guilherme.facebook_id, self.data_user_guilherme["id"])
