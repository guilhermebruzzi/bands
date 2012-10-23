#!/usr/bin/env python
#-*- coding:utf-8 -*-

from unittest import TestCase
from controllers import get_or_create_user, get_or_create_questions
from models import User, Question

class ControllersTest(TestCase):

    def setUp(self):
        self.data_user_guilherme = {"id": "bands2012", "email": "guibruzzi@gmail.com", "name": "Guilherme"}
        self.__delete_all__(User)

        self.questions_txt = ["Voce quer ser meu amigo?", "Voce me ama?"]
        self.__delete_all__(Question)

    def tearDown(self):
        self.__delete_all__(User)
        self.__delete_all__(Question)

    def get_or_create_user_maintain_object_test(self):
        user_guilherme = get_or_create_user(data=self.data_user_guilherme)
        self.__assert_user__(user_guilherme, self.data_user_guilherme)

        user = User.objects.all()[0]
        self.__assert_user__(user, self.data_user_guilherme)

        user_guilherme = get_or_create_user(data=self.data_user_guilherme)
        self.__assert_user__(user_guilherme, self.data_user_guilherme)

    def get_or_create_questions_test(self):
        questions = get_or_create_questions(self.questions_txt)
        self.__assert_questions__(questions, self.questions_txt)

        questions = Question.objects.all()
        self.__assert_questions__(questions, self.questions_txt)

        questions = get_or_create_questions(self.questions_txt)
        self.__assert_questions__(questions, self.questions_txt)

    def __assert_user__(self, user, user_data):
        self.assertEqual(user.facebook_id, user_data["id"])
        self.assertEqual(user.name, user_data["name"])
        self.assertEqual(user.email, user_data["email"])
        self.assertEqual(user.photo, 'http://graph.facebook.com/%s/picture' % user_data["id"])

    def __assert_questions__(self, questions, questions_txt):
        for question in questions:
            self.assertIn(question.question, questions_txt)
            self.assertEqual(question.answers, [])

    def __delete_all__(self,cls):
        for object in cls.objects:
            object.delete()
