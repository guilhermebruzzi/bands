#!/usr/bin/env python
#-*- coding:utf-8 -*-

from unittest import TestCase
from config import get_app

class ConfigTest(TestCase):

    def setUp(self):
        self.app = get_app()

    def assert_config_test(self):
        self.assertEqual(self.app.config['MONGODB_DB'], 'bands_test')
        self.assertEqual(self.app.config['MONGODB_USERNAME'], None)
        self.assertEqual(self.app.config['MONGODB_PASSWORD'], None)
        self.assertEqual(self.app.config['MONGODB_HOST'], 'localhost')
        self.assertEqual(self.app.config['MONGODB_PORT'], 7777)
        self.assertEqual(self.app.config['SECRET_KEY'], 'test key')
        self.assertEqual(self.app.config['DEBUG'], True)
        self.assertEqual(self.app.config['FACEBOOK_APP_ID'], '288328027943629')
        self.assertEqual(self.app.config['FACEBOOK_APP_SECRET'], '84dac36688078a8029aad1dce9f42bb7')
        self.assertEqual(self.app.config['ASSETS_DEBUG'], False)

