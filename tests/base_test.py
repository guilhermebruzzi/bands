#!/usr/bin/env python
#-*- coding:utf-8 -*-

from unittest import TestCase

class BaseTest(TestCase):

    def tearDown(self):
        self.__delete_all__()

    def __delete_all__(self):
        for model in self.models:
            self.__delete_all_of_a_model__(model)

    def __delete_all_of_a_model__(self, model):
        model.drop_collection()