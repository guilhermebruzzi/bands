#!/usr/bin/env python
#-*- coding:utf-8 -*-

from unittest import TestCase
from controllers import *
from config import QUESTIONS_PESQUISA
from models import User, Question, Answer, Band

class ControllersTest(TestCase):

    def setUp(self):
        self.data_user_guilherme = {"id": "bands2012", "email": "guibruzzi@gmail.com", "name": "Guilherme"}
        self.data_user_guto = {"id": "bands2013", "email": "guto@marzagao.com", "name": "Guto"}

        self.__delete_all__(User)
        self.__delete_all__(Question)
        self.__delete_all__(Band)

        self.invalid_vazio = {}
        self.invalid_musico_fa_vazio = {"musico-ou-fa": [""],
                                        "some_slug": ["Some value"]}
        self.invalid_musico_fa = {"musico-ou-fa": ["invalid_option"],
                                  "some_slug": ["Some value"]}

        self.valid_musico = {"musico-ou-fa": ["musico"],
                            "musico-favoritos": [u"The Beatles", u"Chico Buarque"],
                            "musico-favoritos_outros": [u"Cláudia Leitte, Turma do Balão Mágico"],
                            "musico-dificuldades": [u"Vender os ingressos dos meus shows e eventos"],
                            "musico-dificuldades_outros": [u""],
                            "musico-solucao": u""}

        self.valid_fa = {"musico-ou-fa": ["fa"],
                         "fa-favoritos": [u"Foo Fighters"]}

        self.valid_update_fa = {"musico-ou-fa": "fa",
                                "fa-favoritos": [u"Chico Buarque"]}

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
            "fa-favoritos": [u"Foo Fighters"]
        }

        self.empty_answers = {"musico-ou-fa": ["musico"],
                             "musico-favoritos_outros": [u"Cláudia Leitte, Turma do Balão Mágico"],
                             "musico-dificuldades": [u"Vender os ingressos dos meus shows e eventos"],
                             "musico-dificuldades_outros": [u""],
                             "musico-solucao": [u""]}

        self.old_question = [
            {
                "slug": "musico-favoritos",
                "class_name": "musico",
                "type": "checkbox_textarea",
                "question": u"Quais as suas bandas ou músicos favoritos?",
                "answers": sorted([ u"The Beatles",  u"Foo Fighters", u"Los Hermanos", u"Chico Buarque", u"Madonna"]),
                "outros": u"A lista acima contém as mais faladas aqui no site, digite outras que você gosta:"
            }
        ]

        self.data_to_question_change = {
            "musico-favoritos": [u"The Beatles", u"Chico Buarque"],
        }

        self.new_question = [
            {
                "slug": "musico-favoritos",
                "class_name": "musico",
                "type": "checkbox_textarea",
                "question": u"Quais as suas bandas favoritas?",
                "answers": sorted([ u"The Beatles",  u"Foo Fighters", u"Los Hermanos", u"Chico Buarque", u"Madonna"]),
                "outros": u"A lista acima contém as mais faladas aqui no site, digite outras que você gosta:"
            }
        ]

        self.beatles1 = {
            "slug": "beatles",
            "name": "The Beatles",
            "user": self.data_user_guilherme["id"]
        }

        self.chico1 = {
            "slug": "chico",
            "name": "Chico",
            "user": self.data_user_guilherme["id"]
        }

        self.guilherme_bruzzi_real_data_user = {"id": "100000002085352", "email": "guibruzzi@gmail.com", "name": "Guilherme Heynemann Bruzzi"}
        self.access_token = "AAAEGO5mvMs0BALaWzyeh7HiL2aruu2Uxu5oS0gISC4hnD8VHkG05ZAH5fYzCBbnOCsEkZBLI7glTMY6iR3N0BC9i7TXyFqH1uCVW0RNQZDZD"


    def tearDown(self):
        self.__delete_all__(User)
        self.__delete_all__(Question)
        self.__delete_all__(Band)

    def get_or_create_band_test(self):
        result = get_or_create_band(self.beatles1)
        self.assertEqual(result.slug, self.beatles1['slug'])
        self.assertIn(self.beatles1['name'], result.names)
        self.assertIn(self.beatles1['user'], result.users)

        result = get_or_create_band(self.chico1)
        self.assertEqual(result.slug, self.chico1['slug'])
        self.assertIn(self.chico1['name'], result.names)
        self.assertIn(self.chico1['user'], result.users)

        user_guto =  get_or_create_user(data=self.data_user_guto)

        beatles2 = {
            "slug": "beatles",
            "name": "Beatles",
            "user": user_guto.facebook_id
        }
        chico2 = {
            "slug": "chico",
            "name": "Chico",
            "user": user_guto.facebook_id
        }
        chico3 = {
            "slug": "chico",
            "name": "Chico",
            "user": user_guto.facebook_id
        }
        chico4 = {
            "slug": "chico",
            "name": "Chico Buarque",
            "user": user_guto.facebook_id
        }


        result = get_or_create_band(beatles2)
        self.assertEqual(result.slug, beatles2['slug'])
        self.assertIn(self.beatles1['name'], result.names)
        self.assertIn(self.beatles1['user'], result.users)
        self.assertIn(beatles2['name'], result.names)
        self.assertIn(beatles2['user'], result.users)
        self.assertEqual(2, len(result.names))
        self.assertEqual(2, len(result.users))

        result = get_or_create_band(chico2)
        self.assertEqual(result.slug, chico2['slug'])
        self.assertIn(self.chico1['name'], result.names)
        self.assertIn(self.chico1['user'], result.users)
        self.assertIn(chico2['user'], result.users)
        self.assertEqual(1, len(result.names))
        self.assertEqual(2, len(result.users))

        result = get_or_create_band(chico3)
        self.assertEqual(result.slug, chico3['slug'])
        self.assertIn(self.chico1['name'], result.names)
        self.assertIn(self.chico1['user'], result.users)
        self.assertIn(chico2['user'], result.users)
        self.assertEqual(1, len(result.names))
        self.assertEqual(2, len(result.users))

        result = get_or_create_band(chico4)
        self.assertEqual(result.slug, chico4['slug'])
        self.assertIn(self.chico1['name'], result.names)
        self.assertIn(chico4['name'], result.names)
        self.assertIn(self.chico1['user'], result.users)
        self.assertIn(chico2['user'], result.users)
        self.assertEqual(2, len(result.names))
        self.assertEqual(2, len(result.users))

    def get_top_bands_assert_empty_if_none_on_bd(self):
        top_bands = get_top_bands()
        self.assertEqual(len(top_bands), 0)

    def get_top_bands_select_all_test(self):
        beatles1 = get_or_create_band(self.beatles1)
        for i in range(10):
            facebook_id = "bands_facebook_id_%d" % i
            beatles1.users.append(facebook_id)
        beatles1.save()
        chico1 = get_or_create_band(self.chico1)

        top_bands = get_top_bands()
        top_bands_slug = [band.slug for band in top_bands]

        self.assertEqual(len(top_bands), 2)
        self.assertIn(beatles1.slug, top_bands_slug)
        self.assertIn(chico1.slug, top_bands_slug)

    def get_top_bands_select_10_from_100(self):
        all_bands = []
        for i in range(100):
            beatles_model = {
                "slug": "beatles%d" % i,
                "name": "The Beatles",
                "user": self.data_user_guilherme["id"]
            }
            all_bands.append(get_or_create_band(beatles_model))

        top_bands = get_top_bands(max=10)

        self.assertEqual(len(top_bands), 10)

        all_bands_slugs = [band.slug for band in all_bands]
        for band in top_bands:
            self.assertIn(band.slug, all_bands_slugs)



    def get_random_users_test(self):
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

        self.assertEqual(users_random[0].name, "User") # Pega apenas o primeiro nome

        users_emails = [user.email for user in users]

        for user_random in users_random:
            self.assertIn(user_random.email, users_emails)

    def get_max_greater_than_number_of_users_test(self):
        users = []
        for user_id in range(7):
            user = get_or_create_user(data={"id": "id%d" % user_id, "email": "user%d@gmail.com" % user_id, "name": "User %d" % user_id})
            users.append(user)

        users_random, len_users = get_random_users(max=8)

        users_emails = [user.email for user in users_random]

        self.assertEqual(len_users, 7)
        self.assertEqual(len(users_emails), len_users)
        self.assertEqual(len(users_emails), len(set(users_emails)))

        self.assertEqual(users_random[0].name, "User") # Pega apenas o primeiro nome


    def get_random_unique_users_test(self):
        users = []
        for user_id in range(21):
            user = get_or_create_user(data={"id": "id%d" % user_id, "email": "user%d@gmail.com" % user_id, "name": "User %d" % user_id})
            users.append(user)

        users_random, len_users = get_random_users(max=20)

        users_emails = [user.email for user in users_random]
        self.assertEqual(len(users_emails), len(set(users_emails))) # Sem pessoas repetidas


    def save_answers_test(self):
        user_guilherme = get_or_create_user(data=self.data_user_guilherme)
        save_answers(self.valid_musico, user_guilherme)
        self.__assert_answers__("musico-ou-fa", user_guilherme, "musico")
        self.__assert_answers__("musico-favoritos", user_guilherme, [u"The Beatles", u"Chico Buarque", u"Cláudia Leitte, Turma do Balão Mágico"])
        self.__assert_answers__("musico-favoritos_outros", user_guilherme, [])
        self.__assert_answers__("musico-dificuldades", user_guilherme, u"Vender os ingressos dos meus shows e eventos")
        self.__assert_answers__("musico-dificuldades_outros", user_guilherme, [])
        self.__assert_answers__("musico-solucao", user_guilherme, [])

        user_guto =  get_or_create_user(data=self.data_user_guto)
        save_answers(self.valid_fa, user_guto)
        self.__assert_answers__("musico-ou-fa", user_guto, "fa")
        self.__assert_answers__("fa-favoritos", user_guto, u"Foo Fighters")


    def change_text_of_a_question_test(self):
        user_guilherme = get_or_create_user(data=self.data_user_guilherme)
        save_answers(self.data_to_question_change, user_guilherme, self.old_question)
        question = get_question("musico-favoritos")
        self.assertEqual(question.question, u"Quais as suas bandas ou músicos favoritos?")

        save_answers(self.data_to_question_change, user_guilherme, self.new_question)
        question = get_question("musico-favoritos")
        self.assertEqual(question.question, u"Quais as suas bandas favoritas?")


    def dont_save_empty_answers_test(self):
        user_guilherme = get_or_create_user(data=self.data_user_guilherme)
        save_answers(self.valid_musico, user_guilherme)
        self.assertEqual(get_question("musico-favoritos_outros"), None)
        self.assertEqual(get_question("musico-dificuldades_outros"), None)
        self.assertEqual(get_question("musico-solucao"), None)


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


    def sort_and_make_unique_answers_test(self):
        user_guilherme = get_or_create_user(data=self.data_user_guilherme)
        user_guto = get_or_create_user(data=self.data_user_guto)

        answer1 = Answer()
        answer1.user = user_guilherme
        answer1.answer = "First answer"

        answer2 = Answer()
        answer2.user = user_guilherme
        answer2.answer = "Duplicated answer"

        answer3 = Answer()
        answer3.user = user_guto
        answer3.answer = "Duplicated answer"

        answer4 = Answer()
        answer4.user = user_guto
        answer4.answer = "Last test"

        answer_instances = [answer1, answer2, answer3, answer4]
        expected = ["Duplicated answer", "First answer", "Last test"]
        self.assertEqual(sort_and_make_unique_answers(answer_instances), expected)



    def get_or_create_users_test(self):
        user_guilherme = get_or_create_user(data=self.data_user_guilherme)
        self.__assert_user__(user_guilherme, self.data_user_guilherme)

        bands = Band.objects.all() #  Ao criar um usuário, vejo se ele inseriu bandas sem eu querer isso
        self.assertEqual(len(bands), 0)

        user = User.objects.all()[0]
        self.__assert_user__(user, self.data_user_guilherme)

        user_guilherme = get_or_create_user(data=self.data_user_guilherme)
        self.__assert_user__(user_guilherme, self.data_user_guilherme)

    def get_or_create_user_and_his_bands(self):
        get_or_create_user(data=self.guilherme_bruzzi_real_data_user, oauth_token=self.access_token)
        bands = Band.objects.all()
        self.assertGreater(len(bands), 0)
        bands_names = [band.names[0] for band in bands]
        self.assertIn("Foo Fighters", bands_names)

    def get_user_bands_test(self):
        user_guilherme = get_or_create_user(data=self.data_user_guilherme)
        get_or_create_band(self.beatles1)
        get_or_create_band(self.chico1)

        bands = get_user_bands(facebook_id=user_guilherme.facebook_id)
        bands_slug = [band.slug for band in bands]

        self.assertEqual(len(bands), 2)
        self.assertIn(self.beatles1["slug"], bands_slug)
        self.assertIn(self.chico1["slug"], bands_slug)


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
