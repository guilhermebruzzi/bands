#!/usr/bin/env python
#-*- coding:utf-8 -*-

from base_test import BaseTest

from lastfm import save_next_shows, get_nearby_shows
from controllers import get_or_create_band
from models import Band, Show, Location

class LastFmTest(BaseTest):

    models = [Band, Show, Location] #  A serem deletados a cada teste

    def setUp(self):
        self.__delete_all__() #  Chama a funcao que deleta todos os models que essa classe testa

        self.artists = ["Franz Ferdinand", "Ivete Sangalo", "Chico Buarque", "Muse"]
        self.bands = [get_or_create_band({"name": artist}) for artist in self.artists]

    def save_next_shows_test(self):
        shows_returned = save_next_shows(self.bands)

        shows = Show.objects.all()
        locations = Location.objects.all()

        self.assertNotEqual(len(shows), 0)
        self.assertEqual(len(shows_returned), len(shows))
        self.assertNotEqual(len(locations), 0)

        self.__assert_shows__(shows, shows_titles=None)

    def get_nearby_shows_test(self):
        shows = get_nearby_shows(city="Rio de Janeiro")
        shows_from_mongo = Show.objects.all()

        self.assertEqual(len(shows), len(shows_from_mongo))

        self.__assert_shows__(shows, shows_titles=None)

    def get_band_data_test(self):
        franz = self.bands[0]
        self.assertEqual(franz.photo_url, None)
        self.assertEqual(franz.tags_list, [])

        self.assertEqual(franz.photo, "http://userserve-ak.last.fm/serve/252/7149.jpg")
        self.assertEqual(franz.tags, ["indie", "indie rock", "rock", "alternative", "britpop"])

        self.assertEqual(franz.photo_url, "http://userserve-ak.last.fm/serve/252/7149.jpg")
        self.assertEqual(franz.tags_list, ["indie", "indie rock", "rock", "alternative", "britpop"])

        franz_from_mongo = Band.objects.get(name="Franz Ferdinand")
        self.assertEqual(franz_from_mongo.photo_url, "http://userserve-ak.last.fm/serve/252/7149.jpg")
        self.assertEqual(franz_from_mongo.photo, "http://userserve-ak.last.fm/serve/252/7149.jpg")

        self.assertEqual(franz_from_mongo.tags_list, ["indie", "indie rock", "rock", "alternative", "britpop"])
        self.assertEqual(franz_from_mongo.tags, ["indie", "indie rock", "rock", "alternative", "britpop"])

        self.assertIn("Franz Ferdinand", franz_from_mongo.history_content)
        self.assertIn("Franz Ferdinand", franz_from_mongo.history)


