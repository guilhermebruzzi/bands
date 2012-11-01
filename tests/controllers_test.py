#!/usr/bin/env python
#-*- coding:utf-8 -*-

from unittest import TestCase
from controllers import *
from config import QUESTIONS_PESQUISA
from models import User, Question, Answer

class ControllersTest(TestCase):

    def setUp(self):
        self.data_user_guilherme = {"id": "bands2012", "email": "guibruzzi@gmail.com", "name": "Guilherme"}
        self.data_user_guto = {"id": "bands2013", "email": "guto@marzagao.com", "name": "Guto"}
        self.__delete_all__(User)

        self.questions_txt = ["Voce quer ser meu amigo?", "Voce me ama?"]
        self.__delete_all__(Question)

        self.invalid_data1 = {}
        self.invalid_data2 = {"answer_main": "", "answers0": "Some value"}
        self.invalid_data3 = {"answer_main": "invalid_option", "answers0": "Some value"}

        self.valid_data1 = {"answer_main": "musico", "answers0": ["Answer0-0", "Answer0-1"],
                            "answers_outros0": "Answer_outros0-0, Answer_outros0-1",
                            "answers1": "Answer1",
                            "answers_outros1": "Answer_outros1-0, Answer_outros1-1",
                            "answers2": "Answer2", "answers3": "Answer3", "answers4": ""}

        self.valid_data2 = {"answer_main": "fa", "answers5": "Answer0", "answers7": "Answer2",
                            "answers_outros7": "Answer_outros7-0, Answer_outros7-1"}


    def tearDown(self):
        self.__delete_all__(User)
        self.__delete_all__(Question)


    def save_answers_test(self):
        user_guilherme = get_or_create_user(data=self.data_user_guilherme)

        save_answers(self.valid_data1, user_guilherme)
        self.__assert_answers__(question=self.__get_question__(pos=0),
            answers_users=[("Answer0-0", user_guilherme), ("Answer0-1", user_guilherme),
                           ("Answer_outros0-0, Answer_outros0-1", user_guilherme)])
        self.__assert_not_answers__(question=self.__get_question__(pos=4),
            answers_users=[("", user_guilherme)]) #  answers4: ""

        user_guto =  get_or_create_user(data=self.data_user_guto)
        save_answers(self.valid_data2, user_guto)
        self.__assert_answers__(question=self.__get_question__(pos=5),
            answers_users=[("Answer0", user_guto)])
        self.__assert_answers__(question=self.__get_question__(pos=7),
            answers_users=[("Answer2", user_guto), ("Answer_outros7-0, Answer_outros7-1", user_guto)])
        self.__assert_not_answers__(question=self.__get_question__(pos=6),
            answers_users=[("", user_guilherme)]) #  answers6 não estando presente

        answers = get_all_answers_from_question(u"Quais as suas bandas (ou músicos) favoritas?")
        number_of_answers = len(answers)
        self.assertEqual(number_of_answers, 4) #  pos=0 (3 answers) + pos=5 (1 answer)

        # If i ask to save again, it has to maintain the number os answers
        save_answers(self.valid_data2, user_guto)
        answers = get_all_answers_from_question(u"Quais as suas bandas (ou músicos) favoritas?")
        self.assertEqual(len(answers), number_of_answers)

        # If i ask to save with a different user, then they are different answers
        save_answers(self.valid_data2, user_guilherme)
        answers = get_all_answers_from_question(u"Quais as suas bandas (ou músicos) favoritas?")
        self.assertEqual(len(answers), number_of_answers + 1)

        self.__assert_answers__(question=self.__get_question__(pos=5),
            answers_users=[("Answer0", user_guilherme)])


    def get_all_answers_test(self):
        user_guilherme = get_or_create_user(data=self.data_user_guilherme)
        save_answers(self.valid_data1, user_guilherme)

        user_guto = get_or_create_user(data=self.data_user_guto)
        save_answers(self.valid_data2, user_guto)

        questions_and_all_answers = get_questions_and_all_answers()

        self.assertIn("question", questions_and_all_answers[0].keys())
        self.assertIn("answers", questions_and_all_answers[0].keys())

        self.assertEqual(len(questions_and_all_answers), 5)

        self.assertEqual(questions_and_all_answers[0]["answers"][0], "Answer0") #  alfabetic order
        self.assertEqual(questions_and_all_answers[0]["question"], u"Quais as suas bandas (ou músicos) favoritas?")
        self.assertEqual(questions_and_all_answers[3]["answers"][0], "Answer3") #  alfabetic order
        self.assertEqual(questions_and_all_answers[3]["question"], u"Quais as funcionalidades mais importantes que você gostaria que tivesse no site?")
        self.assertEqual(questions_and_all_answers[4]["answers"][1], "Answer_outros7-0, Answer_outros7-1") #  alfabetic order
        self.assertEqual(questions_and_all_answers[4]["question"], u"Que nome para esse produto você gosta mais?")


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


    def __get_question__(self, pos):
        return QUESTIONS_PESQUISA[pos]["question"]


    def __get_answers_users_from_mongo__(self, question):
        answers_users_from_mongo = []
        answers_from_mongo = get_all_answers_from_question(question)
        for answer_from_mongo in answers_from_mongo:
            answer_user_from_mongo = (answer_from_mongo.answer, answer_from_mongo.user)
            answers_users_from_mongo.append(answer_user_from_mongo)
        return answers_users_from_mongo


    def __assert_answers__(self, question, answers_users):
        answers_users_from_mongo = self.__get_answers_users_from_mongo__(question)

        for answer_user in answers_users:
            self.assertIn(answer_user, answers_users_from_mongo)


    def __assert_not_answers__(self, question, answers_users):
        answers_users_from_mongo = self.__get_answers_users_from_mongo__(question)

        for answer_user in answers_users:
            self.assertNotIn(answer_user, answers_users_from_mongo)


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
