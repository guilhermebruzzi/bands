#!/usr/bin/env python
#-*- coding:utf-8 -*-

from unittest import TestCase
from models import Band, Location

class BaseTest(TestCase):

    def tearDown(self):
        self.__delete_all__()

    def __delete_all__(self):
        for model in self.models:
            self.__delete_all_of_a_model__(model)

    def __delete_all_of_a_model__(self, model):
        model.drop_collection()

    def __assert_shows__(self, shows, shows_titles=None):
        self.assertNotEqual(len(shows), 0)
        if shows_titles:
            titles = [show.title for show in shows]
            for show_title in shows_titles:
                self.assertIn(show_title, titles)
        for show in shows:
            self.assertTrue(isinstance(show.artists[0], Band), msg="Pega os artistas do lastfm como bandas nossas")
            self.assertTrue(isinstance(show.location, Location), msg="Pega o local do lastfm como uma classe Location nossa")
            self.assertRegexpMatches(show.datetime, r"(\d{2})/(\d{2})/(\d{4}) (\d{2}):(\d{2}):(\d{2})")