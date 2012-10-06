#!/usr/bin/env python
#-*- coding:utf-8 -*-

from unittest import TestCase
from helpers import get_slug

class HelpersTest(TestCase):

    def get_slug_test(self):
        title = "Whos Using It?"
        slug = get_slug(title)
        self.assertEqual(slug, "whos-using-it")

    def get_slug_com_acento_test(self):
        title = "Este é um outro teste ÉÁÃ"
        slug = get_slug(title)
        self.assertEqual(slug, "este-e-um-outro-teste-eaa")
