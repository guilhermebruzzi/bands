#!/usr/bin/env python
#-*- coding:utf-8 -*-

import unittest
import time
from splinter import Browser

class TestAceitacao(unittest.TestCase):

    def setUp(self):
        pass

    def login_facebook(self, browser):
        browser.visit('http://localhost:5000/')
        button_login_fb = browser.find_by_css('.login-menu-facebook').first
        button_login_fb.click()
        time.sleep(3)
        browser.fill('email', 'guilherme.bruzzi@corp.globo.com')
        browser.fill('pass', 'perfilteste')
        browser.find_by_id('u_0_1').click()
        opcao_musico = browser.find_by_id('musico-ou-fa0')
        if opcao_musico:
            opcao_musico.click()
            browser.find_by_id('salvar-cadastro').click()
        self.assertTrue(browser.url.startswith('http://localhost:5000/minhas-bandas'), msg=u"Entrou em minhas bandas corretamente após processo completo de login")

    def test_login_logout(self):
        with Browser() as browser:
            browser.driver.maximize_window()
            self.login_facebook(browser)
            browser.visit('http://localhost:5000/')
            button_login_fb = browser.find_by_css('.login-facebook')
            self.assertEqual(len(button_login_fb), 0, msg=u"A pessoa está corretamente logada")
            browser.find_by_id('user-box-options').click()
            browser.find_by_css('.menu-lista a')[2].click() #  Clicar no logout
            browser.find_by_css('.login-menu-facebook').click() # relogar
            self.assertTrue(browser.url.startswith('http://localhost:5000/minhas-bandas'), msg=u"Entrou em minhas bandas corretamente após se relogar")

    def pesquisa_e_expande_foo_fighters(self, browser):
        browser.visit('http://localhost:5000/')
        opcoes_procurar = browser.find_by_id("opcoes-procurar-bandas-text")
        opcoes_procurar.type('Foo Fighters\n')
        time.sleep(3)
        self.assertEqual(browser.find_by_css("#foo-fighters .info-banda-nome").text.upper(), 'FOO FIGHTERS')
        browser.find_by_css("#foo-fighters .info-banda-header").first.click()
        self.assertEqual(browser.find_by_css("#foo-fighters .titulo-timeline-no-box").text.upper(), 'TIMELINE')
        contribuaTimeline = browser.find_by_css('#foo-fighters .contribua-timeline')
        self.assertNotEqual(len(contribuaTimeline), 0)
        contribuaTimeline.first.click()
        self.assertIn('contato@bands.com.br', browser.find_by_css("#modal-contribuicao-foo-fighters .modal-body p").text)

    def test_pesquisa_e_expande_timeline(self):
        with Browser() as browser:
            browser.driver.maximize_window()
            self.pesquisa_e_expande_foo_fighters(browser)
            self.login_facebook(browser)
            self.pesquisa_e_expande_foo_fighters(browser)

if __name__ == '__main__':
    unittest.main()
