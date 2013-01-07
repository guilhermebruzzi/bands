#!/usr/bin/env python
#-*- coding:utf-8 -*-

from base_test import BaseTest

from lastfm import save_next_shows
from controllers import get_or_create_band
from models import Band, Show, Location

class FacebookTest(BaseTest):

    models = [Band, Show, Location] #  A serem deletados a cada teste

    def setUp(self):
        self.__delete_all__() #  Chama a funcao que deleta todos os models que essa classe testa

        self.artists = ["Foo Fighters", "Los Hermanos", "Chico Buarque", "Muse"]
        self.bands = [get_or_create_band({"name": artist}) for artist in self.artists]

    def save_next_shows_test(self):
        save_next_shows(self.bands, limit_per_artist=1)

        shows = Show.objects.all()
        locations = Location.objects.all()

        self.assertNotEqual(len(shows), 0)
        self.assertNotEqual(len(locations), 0)

        self.assertNotEqual(len(shows[0].artists), 0)
        self.assertTrue(isinstance(shows[0].artists[0], Band), msg="Pega os artistas do lastfm como bandas nossas")

        self.assertTrue(isinstance(shows[0].location, Location), msg="Pega o local do lastfm como uma classe Location nossa")

        self.assertRegexpMatches(shows[0].datetime, r"(\d{2})/(\d{2})/(\d{4}) (\d{2}):(\d{2}):(\d{2})")
