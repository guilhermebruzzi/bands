#!/usr/bin/env python
#-*- coding:utf-8 -*-

from unittest import TestCase
from controllers import *
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
                            "musico-dificuldades": [u"Vender os ingressos dos meus shows e eventos"],
                            "musico-dificuldades_outros": [u""],
                            "musico-solucao": u""}

        self.valid_musico_funcionalidades = {"musico-funcionalidades": [u"Venda de ingressos"],
                                             "musico-funcionalidades_outros": [u"Outra funcionalidade"]}


        self.valid_fa = {"musico-ou-fa": ["fa"],
                         "fa-funcionalidades": [u"Venda de ingressos"],
                         "fa-funcionalidades_outros": [u"Outra funcionalidade"]}

        self.valid_update_fa = {"musico-ou-fa": "fa",
                                "fa-funcionalidades": [u"Divulgação de shows e eventos"]}

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
            "musico-dificuldades": [u"Vender os ingressos dos meus shows e eventos"],
            "fa-funcionalidades": [u"Venda de ingressos", u"Outra funcionalidade"],
            "musico-funcionalidades": [u"Venda de ingressos", u"Outra funcionalidade"]
        }

        self.expected_result_all_question_and_answers_with_funcionalidades = {
            "musico-ou-fa": ["musico", "fa"],
            "musico-dificuldades": [u"Vender os ingressos dos meus shows e eventos"],
            "fa-funcionalidades": [u"Venda de ingressos", u"Outra funcionalidade"],
            "musico-funcionalidades": [u"Venda de ingressos", u"Outra funcionalidade"],
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
        }
        self.beatles2 = {
            "slug": "BeaTleS",
            "name": "Beatles",
        }

        self.cassia1 = {
            "slug": u"cassia-eller",
            "name": u"Cássia Eller",
        }
        self.cassia2 = {
            "slug": u"cássia Eller",
            "name": u"Cássia Eller",
        }
        self.cassia3 = {
            "slug": u"Cássia eller",
            "name": u"Cássia Eller",
        }
        self.cassia4 = {
            "slug": u"cassia Eller",
            "name": u"Cássia",
        }

        self.guilherme_bruzzi_real_data_user = {"id": "100000002085352", "email": "guibruzzi@gmail.com", "name": "Guilherme Heynemann Bruzzi"}
        self.access_token = "AAAEGO5mvMs0BALaWzyeh7HiL2aruu2Uxu5oS0gISC4hnD8VHkG05ZAH5fYzCBbnOCsEkZBLI7glTMY6iR3N0BC9i7TXyFqH1uCVW0RNQZDZD"

    def tearDown(self):
        self.__delete_all__(User)
        self.__delete_all__(Question)
        self.__delete_all__(Band)

    def like_band_test(self):
        user_guilherme = get_or_create_user(data=self.data_user_guilherme)
        user_guto = get_or_create_user(data=self.data_user_guto)

        self.beatles1['user'] = user_guilherme
        get_or_create_band(self.beatles1)

        result = get_band(self.beatles1['slug'])
        like_band(result.slug, user_guto)

        result = get_band(self.beatles1['slug'])
        self.assertIn(user_guto, result.users)

    def unlike_band_test(self):
        user_guilherme = get_or_create_user(data=self.data_user_guilherme)
        user_guto = get_or_create_user(data=self.data_user_guto)

        self.beatles1['user'] = user_guilherme
        get_or_create_band(self.beatles1)

        self.beatles1['user'] = user_guto
        get_or_create_band(self.beatles1)

        result = get_band(self.beatles1['slug'])
        self.assertIn(user_guilherme, result.users)
        self.assertIn(user_guto, result.users)

        unlike_band(result.slug, user_guilherme)
        result = get_band(self.beatles1['slug'])
        self.assertNotIn(user_guilherme, result.users)

        unlike_band(result.slug, user_guto)
        result = get_band(self.beatles1['slug'])
        self.assertNotIn(user_guto, result.users)

    def get_or_create_band_test(self):
        user_guilherme = get_or_create_user(data=self.data_user_guilherme)
        user_guto = get_or_create_user(data=self.data_user_guto)

        self.beatles1['user'] = user_guilherme
        self.beatles2['user'] = user_guto

        self.cassia1['user'] = user_guilherme
        self.cassia2['user'] = user_guto
        self.cassia3['user'] = user_guto
        self.cassia4['user'] = user_guto

        result = get_or_create_band(self.beatles1)
        self.assertEqual(self.beatles1['slug'], result.slug)
        self.assertEqual(self.beatles1['name'], result.name)
        self.assertIn(self.beatles1['name'], result.aliases)
        self.assertIn(user_guilherme, result.users)
        self.assertEqual(1, len(result.aliases))
        self.assertEqual(1, len(result.users))

        result = get_or_create_band(self.cassia1)
        self.assertEqual(self.cassia1['slug'], result.slug)
        self.assertEqual(self.cassia1['name'], result.name)
        self.assertIn(self.cassia1['name'], result.aliases)
        self.assertIn(user_guilherme, result.users)
        self.assertEqual(1, len(result.aliases))
        self.assertEqual(1, len(result.users))

        result = get_or_create_band(self.beatles2)
        self.assertEqual(self.beatles1['slug'], result.slug)
        self.assertEqual(self.beatles1['name'], result.name)
        self.assertIn(self.beatles1['name'], result.aliases)
        self.assertIn(user_guilherme, result.users)
        self.assertIn(self.beatles2['name'], result.aliases)
        self.assertIn(user_guto, result.users)
        self.assertEqual(2, len(result.aliases))
        self.assertEqual(2, len(result.users))

        result = get_or_create_band(self.cassia2)
        self.assertEqual(self.cassia1['slug'], result.slug)
        self.assertEqual(self.cassia1['name'], result.name)
        self.assertIn(self.cassia1['name'], result.aliases)
        self.assertIn(user_guilherme, result.users)
        self.assertIn(user_guto, result.users)
        self.assertEqual(1, len(result.aliases))
        self.assertEqual(2, len(result.users))

        result = get_or_create_band(self.cassia3)
        self.assertEqual(self.cassia1['slug'], result.slug)
        self.assertEqual(self.cassia1['name'], result.name)
        self.assertIn(self.cassia1['name'], result.aliases)
        self.assertIn(user_guilherme, result.users)
        self.assertIn(user_guto, result.users)
        self.assertEqual(1, len(result.aliases))
        self.assertEqual(2, len(result.users))

        result = get_or_create_band(self.cassia4)
        self.assertEqual(self.cassia1['slug'], result.slug)
        self.assertEqual(self.cassia1['name'], result.name)
        self.assertIn(self.cassia1['name'], result.aliases)
        self.assertIn(user_guilherme, result.users)
        self.assertIn(user_guto, result.users)
        self.assertIn(self.cassia4['name'], result.aliases)
        self.assertEqual(2, len(result.aliases))
        self.assertEqual(2, len(result.users))

    def get_top_bands_test(self):
        bands, total_bands = get_top_bands()
        self.assertEqual(bands, [])
        self.assertEqual(total_bands, 0)

        user_guilherme = get_or_create_user(data=self.data_user_guilherme)
        user_guto = get_or_create_user(data=self.data_user_guto)

        self.beatles1['user'] = user_guilherme
        beatles1 = get_or_create_band(self.beatles1)
        top_bands, total_bands = get_top_bands(sort=True)

        self.assertEqual(len(top_bands), 1)
        self.assertEqual(beatles1.name, top_bands[0]["label"])
        self.assertEqual(1, top_bands[0]["size"])

        self.beatles1['user'] = user_guto
        beatles1 = get_or_create_band(self.beatles1)
        top_bands, total_bands = get_top_bands(sort=True)

        self.assertEqual(len(top_bands), 1)
        self.assertEqual(beatles1.name, top_bands[0]["label"])
        self.assertEqual(2, top_bands[0]["size"])

        self.cassia1['user'] = user_guilherme
        cassia1 = get_or_create_band(self.cassia1)
        top_bands, total_bands = get_top_bands(sort=True)

        self.assertEqual(len(top_bands), 2)
        self.assertEqual(total_bands, 2)
        self.assertEqual(beatles1.name, top_bands[0]["label"])
        self.assertEqual(2, top_bands[0]["size"])
        self.assertEqual(cassia1.name, top_bands[1]["label"])
        self.assertEqual(1, top_bands[1]["size"])

    def get_top_bands_shuffle_and_normalized_test(self):
        user_guilherme = get_or_create_user(data=self.data_user_guilherme)
        user_guto = get_or_create_user(data=self.data_user_guto)

        for user_id in range(12):
            user = get_or_create_user(data={"id": "id%d" % user_id, "email": "user%d@gmail.com" % user_id, "name": "User %d" % user_id})
            self.beatles1['user'] = user
            get_or_create_band(self.beatles1)

        self.cassia1['user'] = user_guilherme
        get_or_create_band(self.cassia1)
        self.cassia1['user'] = user_guto
        get_or_create_band(self.cassia1)

        top_bands, total_bands = get_top_bands(sort=False, normalize=True)

        top_bands_labels = [band["label"] for band in top_bands]
        self.assertIn(self.beatles1["name"], top_bands_labels)
        self.assertIn(self.cassia1["name"], top_bands_labels)

        for band in top_bands:
            if band["label"] == self.beatles1["name"]:
                self.assertEqual(band["size"], 6)
            else:
                self.assertEqual(band["size"], 1)


    def random_top_bands_ignoring_my_liked_bands_test(self):
        user_guilherme = get_or_create_user(data=self.data_user_guilherme)
        user_guto = get_or_create_user(data=self.data_user_guto)

        self.beatles1['user'] = user_guilherme
        self.beatles2['user'] = user_guto

        self.cassia1['user'] = user_guilherme
        self.cassia2['user'] = user_guto

        beatles1 = get_or_create_band(self.beatles1)
        top_bands = random_top_bands(user=user_guto)
        top_bands_slug = [band.slug for band in top_bands]

        self.assertEqual(len(top_bands), 1)
        self.assertIn(beatles1.slug, top_bands_slug)

        cassia1 = get_or_create_band(self.cassia1)
        top_bands = random_top_bands(user=user_guto)
        top_bands_slug = [band.slug for band in top_bands]

        self.assertEqual(len(top_bands), 2)
        self.assertIn(beatles1.slug, top_bands_slug)
        self.assertIn(cassia1.slug, top_bands_slug)

        get_or_create_band(self.beatles2)
        top_bands = random_top_bands(user=user_guto)
        top_bands_slug = [band.slug for band in top_bands]

        self.assertEqual(len(top_bands), 1)
        self.assertIn(cassia1.slug, top_bands_slug)

        get_or_create_band(self.cassia2)
        top_bands = random_top_bands(user=user_guto)
        self.assertEqual(len(top_bands), 0)


    def random_top_bands_assert_empty_if_none_on_bd_test(self):
        top_bands = random_top_bands()
        self.assertEqual(len(top_bands), 0)

    def random_top_bands_select_all_test(self):
        user_guilherme = get_or_create_user(data=self.data_user_guilherme)
        user_guto = get_or_create_user(data=self.data_user_guto)

        self.beatles1['user'] = user_guilherme
        self.beatles2['user'] = user_guto

        self.cassia1['user'] = user_guilherme
        self.cassia2['user'] = user_guto

        beatles1 = get_or_create_band(self.beatles1)
        get_or_create_band(self.beatles2)

        cassia1 = get_or_create_band(self.cassia1)
        get_or_create_band(self.cassia2)

        top_bands = random_top_bands()
        top_bands_slug = [band.slug for band in top_bands]

        self.assertEqual(len(top_bands), 2)
        self.assertIn(beatles1.slug, top_bands_slug)
        self.assertIn(cassia1.slug, top_bands_slug)

    def random_top_bands_select_10_from_100_test(self):
        user_guilherme = get_or_create_user(data=self.data_user_guilherme)

        all_bands = []
        for i in range(100):
            beatles_model = {
                "slug": "beatles%d" % i,
                "name": "The Beatles",
                "user": user_guilherme
            }
            all_bands.append(get_or_create_band(beatles_model))

        top_bands = random_top_bands(max=10)

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
        self.__assert_answers__("musico-dificuldades", user_guilherme, u"Vender os ingressos dos meus shows e eventos")
        self.__assert_answers__("musico-dificuldades_outros", user_guilherme, [])
        self.__assert_answers__("musico-solucao", user_guilherme, [])

        user_guto =  get_or_create_user(data=self.data_user_guto)
        save_answers(self.valid_fa, user_guto)
        self.__assert_answers__("musico-ou-fa", user_guto, "fa")
        self.__assert_answers__("fa-funcionalidades", user_guto, [u"Venda de ingressos", u"Outra funcionalidade"])

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

        answers = get_all_answers_from_question("fa-funcionalidades")
        self.assertEqual(len(answers), 2)

    def saving_same_answer_from_different_users_test(self):
        user_guto =  get_or_create_user(data=self.data_user_guto)
        user_guilherme =  get_or_create_user(data=self.data_user_guilherme)

        save_answers(self.valid_fa, user_guto)
        save_answers(self.valid_fa, user_guilherme)

        answers = get_all_answers_from_question("fa-funcionalidades")
        self.assertEqual(len(answers), 4)

    def saving_different_answers_from_same_user_test(self):
        user_guto =  get_or_create_user(data=self.data_user_guto)

        save_answers(self.valid_fa, user_guto)
        save_answers(self.valid_update_fa, user_guto)

        answers = get_all_answers_from_question("fa-funcionalidades")
        self.assertEqual(len(answers), 3)

    def get_all_answers_test(self):
        user_guilherme = get_or_create_user(data=self.data_user_guilherme)
        save_answers(self.valid_musico, user_guilherme)
        save_answers(self.valid_musico_funcionalidades, user_guilherme)

        user_guto = get_or_create_user(data=self.data_user_guto)
        save_answers(self.valid_fa, user_guto)

        questions_and_answers = get_all_questions_and_all_answers()

        for key, value in self.expected_result.items():
            self.assertIn(key, questions_and_answers.keys())
            self.assertEqual(sorted(value), sorted(questions_and_answers[key]["answers"]))
            question = get_or_create_question({"slug": key})
            self.assertEqual(question, questions_and_answers[key]["question"])
            del questions_and_answers[key]

        self.assertEqual(len(questions_and_answers.values()), 0)

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

    def get_or_create_user_and_his_bands_test(self):
        get_or_create_user(data=self.guilherme_bruzzi_real_data_user, oauth_token=self.access_token)
        bands = Band.objects.all()
        self.assertGreater(len(bands), 0)
        bands_names = [band.aliases[0] for band in bands]
        self.assertIn("Foo Fighters", bands_names)

    def get_user_bands_test(self):
        user_guilherme = get_or_create_user(data=self.data_user_guilherme)
        user_guto = get_or_create_user(data=self.data_user_guto)

        self.beatles1['user'] = user_guilherme
        self.beatles2['user'] = user_guto
        self.cassia1['user'] = user_guilherme

        get_or_create_band(self.beatles1)
        get_or_create_band(self.beatles2)
        get_or_create_band(self.cassia1)

        bands = get_user_bands(user=user_guilherme)
        bands_slug = [band.slug for band in bands]

        self.assertEqual(len(bands), 2)
        self.assertIn(self.beatles1["slug"], bands_slug)
        self.assertIn(self.cassia1["slug"], bands_slug)

        bands = get_user_bands(user=user_guto)
        bands_slug = [band.slug for band in bands]

        self.assertEqual(len(bands), 1)
        self.assertIn(self.beatles1["slug"], bands_slug)

    def get_or_create_questions_test(self):
        get_or_create_questions(self.questions)
        self.__assert_questions__(Question.objects.all(), self.questions)
        first_question = get_or_create_question({"slug": "first-question-slug"})
        self.assertEqual(first_question.question, "first-question")
        self.assertEqual(first_question.slug, "first-question-slug")
        first_question_new = get_or_create_question({"slug": "first-question-slug", "question": "first-question-new"})
        self.assertEqual(first_question_new.question, "first-question-new")
        self.assertEqual(first_question_new.slug, "first-question-slug")

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
