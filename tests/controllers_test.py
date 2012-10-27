#!/usr/bin/env python
#-*- coding:utf-8 -*-

from unittest import TestCase
from controllers import *
from models import User, Question, Answer

class ControllersTest(TestCase):

    def setUp(self):
        self.data_user_guilherme = {"id": "bands2012", "email": "guibruzzi@gmail.com", "name": "Guilherme"}
        self.__delete_all__(User)

        self.questions_txt = ["Voce quer ser meu amigo?", "Voce me ama?"]
        self.__delete_all__(Question)

        self.invalid_data1 = {}
        self.invalid_data2 = {"answer_main": "", "answers0": "Some value"}
        self.invalid_data3 = {"answer_main": "invalid_option", "answers0": "Some value"}

        self.valid_data1 = {"answer_main": "musico", "answers0": ["Answer0-0", "Answer0-1"], "answers1": "Answer1",
                            "answers2": "Answer2", "answers3": "Answer3", "answers4": "Answer4"}

        self.valid_data2 = {"answer_main": "fa", "answers5": "Answer0", "answers6": "Answer1", "answers7": "Answer2"}

    def tearDown(self):
        self.__delete_all__(User)
        self.__delete_all__(Question)

    def create_answers_test(self):
        user_guilherme = get_or_create_user(data=self.data_user_guilherme)

        create_answers(self.valid_data1, user_guilherme)
        answers = get_all_answers_from_question(u"Quais as suas bandas (ou músicos) favoritas?")

        self.assertEqual(answers[0].answer, "Answer0-0")
        self.assertEqual(answers[0].user, user_guilherme)

        self.assertEqual(answers[1].answer, "Answer0-1")
        self.assertEqual(answers[1].user, user_guilherme)

        create_answers(self.valid_data2, user_guilherme)
        answers = get_all_answers_from_question(u"Quais as suas bandas (ou músicos) favoritas?")

        self.assertEqual(answers[2].answer, "Answer0")
        self.assertEqual(answers[2].user, user_guilherme)

    def get_or_create_users_test(self):
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

    def get_question_and_his_answer_test(self):
        question_txt = self.questions_txt[0]

        question_mongo = get_or_create_questions(self.questions_txt)[0]

        question = get_question(question_txt)
        answers = get_all_answers_from_question(question_txt)

        self.assertEqual(question.question, question_txt)
        self.assertEqual(question.question, question_mongo.question)
        self.assertEqual(question.answers, answers)

    def validate_answers_test(self):
        self.assertFalse(validate_answers(self.invalid_data1))
        self.assertFalse(validate_answers(self.invalid_data2))
        self.assertFalse(validate_answers(self.invalid_data3))
        self.assertTrue(validate_answers(self.valid_data1))
        self.assertTrue(validate_answers(self.valid_data2))

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
