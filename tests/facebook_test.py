#!/usr/bin/env python
#-*- coding:utf-8 -*-

import flask
from unittest import TestCase
from facebook import get_musicians_from_opengraph
from config import get_app
from models import User
from app import app

class FacebookTest(TestCase):

    def setUp(self):
        self.app = app # Iguala ao flask completo
        self.guilherme_bruzzi_facebook_id = "100000002085352"
        self.access_token = "AAAEGO5mvMs0BALaWzyeh7HiL2aruu2Uxu5oS0gISC4hnD8VHkG05ZAH5fYzCBbnOCsEkZBLI7glTMY6iR3N0BC9i7TXyFqH1uCVW0RNQZDZD"


    def get_musicians_from_opengraph_test(self):
        musicians = get_musicians_from_opengraph(self.guilherme_bruzzi_facebook_id, self.access_token)
        self.assertEqual(type(musicians), list)
        self.assertIn("Foo Fighters", musicians)
