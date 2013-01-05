#!/usr/bin/env python
#-*- coding:utf-8 -*-

from unittest import TestCase
from lastfm import get_next_shows
from models import Band

class FacebookTest(TestCase):

    def setUp(self):
        self.artists = ["Foo Fighters", "Los Hermanos", "Chico Buarque", "Muse"]

    def get_next_shows_test(self):
        shows = get_next_shows(self.artists, limit_per_artist=2)
        self.assertNotEqual(len(shows), 0)

        self.assertIn('artists', shows[0])
        self.assertNotEqual(len(shows[0]['artists']), 0)
        self.assertTrue(isinstance(shows[0]['artists'][0], Band), msg="Pega os artistas do lastfm como bandas nossas")

        self.assertIn('attendance_count', shows[0])
        self.assertEqual(int, type(shows[0]['attendance_count']))

        self.assertIn('data', shows[0])
        self.assertRegexpMatches(shows[0]['data'], r"(\d{2})/(\d{2})/(\d{4}) (\d{2}):(\d{2}):(\d{2})")

        self.assertIn('cover_image', shows[0])
        self.assertIn('title', shows[0])
        self.assertIn('description', shows[0])

