#!/usr/bin/env python
#-*- coding:utf-8 -*-

from unittest import TestCase

from wiki_extract.wiki_extract import wiki_extract

class ControllersTest(TestCase):

    def setUp(self):
        pass

    def wiki_extract_test(self):
        los_hermanos_dict = wiki_extract("Los Hermanos")
        self.assertIn("resumo", los_hermanos_dict.keys())
        self.assertIn("formacao", los_hermanos_dict.keys())
        self.assertIn("Los Hermanos", los_hermanos_dict["resumo"])
        self.assertIn("Marcelo Camelo", los_hermanos_dict["formacao"]["text"])