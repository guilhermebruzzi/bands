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

        self.franz_similares_data = [ "Kaiser Chiefs", "Arctic Monkeys", "The Strokes"]
        self.franz_similares_slug = [ "kaiser-chiefs", "arctic-monkeys", "the-strokes"]

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
        self.assertEqual(franz.similares_slug, [])

        franz_url_photo = "http://userserve-ak.last.fm/serve/252/887131.jpg"

        self.assertEqual(franz.photo, franz_url_photo)
        self.assertEqual(franz.tags, ["indie", "indie rock", "rock", "alternative", "britpop"])
        self.__assert_bands_list__(franz.similares, self.franz_similares_data)

        self.assertEqual(franz.photo_url, franz_url_photo)
        self.assertEqual(franz.tags_list, ["indie", "indie rock", "rock", "alternative", "britpop"])
        self.__assert_bands_slugs__(franz.similares_slug, self.franz_similares_slug)

        franz_from_mongo = Band.objects.get(name="Franz Ferdinand")
        self.assertEqual(franz_from_mongo.photo_url, franz_url_photo)
        self.assertEqual(franz_from_mongo.photo, franz_url_photo)

        self.assertEqual(franz_from_mongo.tags_list, ["indie", "indie rock", "rock", "alternative", "britpop"])
        self.assertEqual(franz_from_mongo.tags, ["indie", "indie rock", "rock", "alternative", "britpop"])

        self.__assert_bands_slugs__(franz_from_mongo.similares_slug, self.franz_similares_slug)
        self.__assert_bands_list__(franz_from_mongo.similares, self.franz_similares_data)

        self.assertIn("Franz Ferdinand", franz_from_mongo.history_content)
        self.assertIn("Franz Ferdinand", franz_from_mongo.history)

    def __assert_bands_list__(self, bands_list, bands_list_data):
        band_names = [band.name for band in bands_list]

        for name in bands_list_data:
            self.assertIn(name, band_names)

    def __assert_bands_slugs__(self, band_slugs, bands_list_data):
        for slug in bands_list_data:
            self.assertIn(slug, band_slugs)
