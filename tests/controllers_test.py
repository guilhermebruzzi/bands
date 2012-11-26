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

        self.invalid_vazio = {}
        self.invalid_musico_fa_vazio = {"musico-ou-fa": "",
                                        "some_slug": "Some value"}
        self.invalid_musico_fa = {"musico-ou-fa": "invalid_option",
                                  "some_slug": "Some value"}

        self.valid_musico = {"musico-ou-fa": "musico",
                            "musico-favoritos": [u"The Beatles", u"Chico Buarque"],
                            "musico-favoritos_outros": u"Cláudia Leitte, Turma do Balão Mágico",
                            "musico-dificuldades": u"Vender os ingressos dos meus shows e eventos",
                            "musico-dificuldades_outros": u"",
                            "musico-solucao": u"",
                            "musico-nome": u"Bands"}

        self.valid_fa = {"musico-ou-fa": "fa",
                         "fa-favoritos": u"Foo Fighters",
                         "fa-nome": "Bands",
                         "fa-nome_outros": "Outro nome, Mais um nome"}

        self.valid_update_fa = {"musico-ou-fa": "fa",
                                "fa-favoritos": u"Chico Buarque",
                                "fa-nome": "Know Your Band",
                                "fa-nome_outros": "Outros nomes"}

        self.questions = [
            {
                "slug": "first-question-slug",
                "question": "first-question",
            },
            {
                "slug": "second-question-slug",
                "question": "second-question",
            }
        ]

        self.expected_result = {
            "musico-ou-fa": ["musico", "fa"],
            "musico-favoritos": [u"The Beatles", u"Chico Buarque", u"Cláudia Leitte, Turma do Balão Mágico"],
            "musico-dificuldades": [u"Vender os ingressos dos meus shows e eventos"],
            "musico-nome": [u"Bands"],
            "fa-favoritos": [u"Foo Fighters"],
            "fa-nome": ["Bands", "Outro nome, Mais um nome"],
        }


    def tearDown(self):
        self.__delete_all__(User)
        self.__delete_all__(Question)

    def get_random_users_test(self, max=8):
        users_random, len_users = get_random_users()
        self.assertEqual(len(users_random), 0)
        self.assertEqual(len_users, 0)

        users = []
        for user_id in range(10):
            user = get_or_create_user(data={"id": "id%d" % user_id, "email": "user%d@gmail.com" % user_id, "name": "User %d" % user_id})
            users.append(user)

        users_random, len_users = get_random_users()

        self.assertEqual(len(users_random), 8)
        self.assertEqual(len_users, len(users))

        self.assertEqual(users_random[0].name, "User")

        for user_random in users_random:
            self.assertIn(user_random.email, [user.email for user in users])


    def save_answers_test(self):
        user_guilherme = get_or_create_user(data=self.data_user_guilherme)
        save_answers(self.valid_musico, user_guilherme)
        self.__assert_answers__("musico-ou-fa", user_guilherme, "musico")
        self.__assert_answers__("musico-favoritos", user_guilherme, [u"The Beatles", u"Chico Buarque", u"Cláudia Leitte, Turma do Balão Mágico"])
        self.__assert_answers__("musico-favoritos_outros", user_guilherme, [])
        self.__assert_answers__("musico-dificuldades", user_guilherme, u"Vender os ingressos dos meus shows e eventos")
        self.__assert_answers__("musico-dificuldades_outros", user_guilherme, [])
        self.__assert_answers__("musico-solucao", user_guilherme, [])
        self.__assert_answers__("musico-nome", user_guilherme, u"Bands")

        user_guto =  get_or_create_user(data=self.data_user_guto)
        save_answers(self.valid_fa, user_guto)
        self.__assert_answers__("musico-ou-fa", user_guto, "fa")
        self.__assert_answers__("fa-favoritos", user_guto, u"Foo Fighters")
        self.__assert_answers__("fa-nome", user_guto, [u"Bands", "Outro nome, Mais um nome"])
        self.__assert_answers__("fa-nome_outros", user_guto, [])


    def not_saving_duplicated_answers_test(self):
        user_guto =  get_or_create_user(data=self.data_user_guto)
        save_answers(self.valid_fa, user_guto)
        save_answers(self.valid_fa, user_guto)

        answers = get_all_answers_from_question("fa-favoritos")
        self.assertEqual(len(answers), 1)


    def saving_same_answer_from_different_users_test(self):
        user_guto =  get_or_create_user(data=self.data_user_guto)
        user_guilherme =  get_or_create_user(data=self.data_user_guilherme)

        save_answers(self.valid_fa, user_guto)
        save_answers(self.valid_fa, user_guilherme)

        answers = get_all_answers_from_question("fa-favoritos")
        self.assertEqual(len(answers), 2)


    def saving_different_answers_from_same_user_test(self):
        user_guto =  get_or_create_user(data=self.data_user_guto)

        save_answers(self.valid_fa, user_guto)
        save_answers(self.valid_update_fa, user_guto)

        answers = get_all_answers_from_question("fa-favoritos")
        self.assertEqual(len(answers), 2)


    def get_all_answers_test(self):
        user_guilherme = get_or_create_user(data=self.data_user_guilherme)
        save_answers(self.valid_musico, user_guilherme)

        user_guto = get_or_create_user(data=self.data_user_guto)
        save_answers(self.valid_fa, user_guto)

        questions_and_answers = get_all_questions_and_all_answers()

        for key, value in self.expected_result.items():
            self.assertEqual(sorted(value), sorted(questions_and_answers[key]))
            del questions_and_answers[key]

        for value in questions_and_answers.values():
            self.assertEqual(value, [])


    def get_or_create_users_test(self):
        user_guilherme = get_or_create_user(data=self.data_user_guilherme)
        self.__assert_user__(user_guilherme, self.data_user_guilherme)

        user = User.objects.all()[0]
        self.__assert_user__(user, self.data_user_guilherme)

        user_guilherme = get_or_create_user(data=self.data_user_guilherme)
        self.__assert_user__(user_guilherme, self.data_user_guilherme)


    def get_or_create_questions_test(self):
        get_or_create_questions(self.questions)
        self.__assert_questions__(Question.objects.all(), self.questions)


    def validate_answers_test(self):
        self.assertFalse(validate_answers(self.invalid_vazio))
        self.assertFalse(validate_answers(self.invalid_musico_fa_vazio))
        self.assertFalse(validate_answers(self.invalid_musico_fa))
        self.assertTrue(validate_answers(self.valid_musico))
        self.assertTrue(validate_answers(self.valid_fa))


    def __assert_answers__(self, slug, user, answers):
        if not type(answers) is (list):
            answers = [answers]

        saved_answers = get_all_answers_from_question(slug, user)
        for answer in answers:
            answerModel = Answer(answer=answer, user=user)
            self.assertIn(answerModel, saved_answers)
            saved_answers.remove(answerModel)

        self.assertEqual(len(saved_answers), 0)


    def __assert_user__(self, user, user_data):
        self.assertEqual(user.facebook_id, user_data["id"])
        self.assertEqual(user.name, user_data["name"])
        self.assertEqual(user.email, user_data["email"])
        self.assertEqual(user.photo, 'http://graph.facebook.com/%s/picture' % user_data["id"])


    def __assert_questions__(self, questionsModel, questions):
        for question in questions:
            self.assertIn(question["slug"], [questionModel.slug for questionModel in questionsModel])


    def __delete_all__(self,cls):
        for object in cls.objects:
            object.delete()
