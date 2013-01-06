#!/usr/bin/env python
#-*- coding:utf-8 -*-

import unittest
from splinter import Browser

class TestAceitacao(unittest.TestCase):

    def setUp(self):
        pass

    def test_login_facebook(self):
        with Browser() as browser:
            browser.visit('localhost:5000/')
            buttons = browser.find_by_css('.login-facebook')
            self.assertEqual(len(buttons), 1)
            button = buttons.first
            button.click()
            self.assertTrue(browser.url.startswith('http://localhost:5000/pesquisa'))

            
if __name__ == '__main__':
    unittest.main()


