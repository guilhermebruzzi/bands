#!/usr/bin/env python
#-*- coding:utf-8 -*-

from datetime import datetime

from base_test import BaseTest

from controllers import *
from models import *

class ControllersTest(BaseTest):

    models = [User, Question, Band, Show, Location, Newsletter, Product, BandQuestion] #  A serem deletados a cada teste

    def setUp(self):
        self.__delete_all__() #  Chama a funcao que deleta todos os models que essa classe testa

        self.data_user_guilherme = {"id": "bands2012", "email": "guibruzzi@gmail.com", "name": "Guilherme"}
        self.data_user_guto = {"id": "bands2013", "email": "guto@marzagao.com", "name": "Guto"}

        self.invalid_vazio = {}
        self.invalid_musico_fa_vazio = {"musico-ou-fa": [""],
                                        "some_slug": ["Some value"]}
        self.invalid_musico_fa = {"musico-ou-fa": ["invalid_option"],
                                  "some_slug": ["Some value"]}

        self.valid_musico = {"musico-ou-fa": "musico",
                            "musico-dificuldades": [u"Vender os ingressos dos meus shows e eventos"],
                            "musico-dificuldades_outros": [u""],
                            "musico-solucao": u""}

        self.valid_musico_funcionalidades = {"musico-funcionalidades": [u"Venda de ingressos"],
                                             "musico-funcionalidades_outros": [u"Outra funcionalidade"]}


        self.valid_fa = {"musico-ou-fa": "fa",
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

        self.coldplay1 = {
            "slug": "coldplay",
            "name": "Coldplay",
        }

        self.legiao = {
            "slug": "legiao-urbana",
            "name": "Legiao Urbana",
        }

        self.lower_letter_band = {
            "slug": "a-banda-mais-bonita-da-cidade",
            "name": "a bAnda maIs bonitA Da ciDade",
            }

        self.guilherme_bruzzi_real_data_user = {"id": "100000002085352", "email": "guibruzzi@gmail.com", "name": "Guilherme Heynemann Bruzzi"}
        self.access_token = 'CAAEGO5mvMs0BABvsScZBfOOjVGP7eWRqlrZCh4ZADonFZC0PT6IyjOQIaKmXtpEUXFaN0oriZAc2hoOLRVppCpFclqKZAhoUbZCxxHiUlqRZAfkLA5WTWghfnpk5CZAvvZCAFBBTOxOZBIz9T6Uu9p23iUU'

        self.maracana_data = {
            'name': "Maracana",
            'city': u"Rio de Janeiro",
            'street': "Maracana street",
            'postalcode': "22010-010",
            'website': "http://www.maracana.com.br",
            'phonenumber': "(21)2222-2222",
            'image': "http://www.maracana.com.br/large.png" #  Large
        }
        self.maracana_slug = "maracana"
        self.morumbi_data = {
            'name': "Morumbi",
            'city': u"São Paulo",
            'street': "SP street",
            'postalcode': "22010-011",
            'website': "http://www.morumbi.com.br",
            'phonenumber': "(15)2222-2222",
            'image': "http://www.morumbi.com.br/large.png" #  Large
        }

        self.product_cd = {
            "name": "CD Los Bife",
            "price": 15,
            "photo": "cd-los-bife.jpg",
            "quantity_type": "list",
            "quantity_value": "pp,p,m,g"
        }
        self.product_camisa = {
            "name": "Camisa Los Bife Amarela",
            "price": 20,
            "photo": "camisa-los-bife-amarela.jpg",
            "quantity_type": "range",
            "quantity_value": "1,10,1"
        }

        self.band_question = {
            "email": "guibruzzi@gmail.com",
            "question": "Quando a Madonna perdeu a virgindade?",
            "band_slug": "madonna"
        }

    def get_all_bands_test(self):
        for band_id in range(12):
            get_or_create_band({"name": "The Beatles %d" % band_id})

        all_bands = get_all_bands()
        self.assertEqual(len(all_bands), 12)
        for band in all_bands:
            self.assertIsInstance(band, Band)

        all_bands_limited = get_all_bands(limit=4)
        self.assertEqual(len(all_bands_limited), 4)
        for index, band in enumerate(all_bands_limited):
            self.assertEqual(band, all_bands[index])

    def timeline_as_dict_test(self):
        beatles_band = get_or_create_band({"name": self.beatles1["name"]})
        timeline = beatles_band.timeline_as_dict()
        self.assertIn("headline", timeline.keys())
        self.assertIn("type", timeline.keys())
        self.assertIn("text", timeline.keys())
        self.assertIn("asset", timeline.keys())
        self.assertEqual(timeline["asset"]["media"], beatles_band.photo_url)
        self.assertIn("date", timeline.keys())
        self.assertEqual(timeline["date"][-1]["startDate"], str(datetime.now().date()).replace("-", ","))

    def get_or_create_band_question_test(self):
        madonna_question = get_or_create_band_question(data=self.band_question)
        self.__assert_question__(madonna_question, self.band_question)

        band_question = BandQuestion.objects.all()[0]
        self.__assert_question__(band_question, self.band_question)

        band_question = get_or_create_band_question(data=self.band_question)
        self.__assert_question__(band_question, self.band_question)
        self.assertEqual(len(BandQuestion.objects.all()), 1)


    def create_user_with_city_test(self):
        self.data_user_guto["city"] = "Rio de Janeiro"
        user_guto = get_or_create_user(data=self.data_user_guto)
        user_guto_from_mongo = User.objects.all()[0]
        self.__assert_user__(user_guto, self.data_user_guto)
        self.__assert_user__(user_guto_from_mongo, self.data_user_guto)

    def update_city_when_getting_user_test(self):
        get_or_create_user(data=self.data_user_guto)
        self.data_user_guto["city"] = "Rio de Janeiro"
        user_guto = get_or_create_user(data=self.data_user_guto)
        user_guto_from_mongo = User.objects.all()[0]
        self.__assert_user__(user_guto, self.data_user_guto)
        self.__assert_user__(user_guto_from_mongo, self.data_user_guto)

    def name_of_band_with_upper_letter_test(self):
        user_guto = get_or_create_user(data=self.data_user_guto)
        self.lower_letter_band['user'] = user_guto
        upper_letter_band = get_or_create_band(self.lower_letter_band)

        self.assertEqual("A Banda Mais Bonita Da Cidade", upper_letter_band.name)

    def get_related_bands_test(self):
        user_guilherme = get_or_create_user(data=self.data_user_guilherme)
        user_guto = get_or_create_user(data=self.data_user_guto)

        self.beatles1['user'] = user_guilherme
        beatles = get_or_create_band(self.beatles1)

        self.cassia1['user'] = user_guto
        cassia = get_or_create_band(self.cassia1)

        self.assertEqual([], get_related_bands(band=beatles))
        self.assertEqual([], get_related_bands(band=cassia))

        self.beatles1['user'] = user_guto
        beatles = get_or_create_band(self.beatles1)

        self.assertEqual([beatles.slug], get_related_bands(band=cassia))
        self.assertEqual([cassia.slug], get_related_bands(band=beatles))

        self.coldplay1['user'] = user_guilherme
        coldplay = get_or_create_band(self.coldplay1)

        self.assertEqual([beatles.slug], get_related_bands(band=coldplay))
        self.assertEqual([beatles.slug], get_related_bands(band=cassia))

        related_bands = get_related_bands(band=beatles)
        self.assertEqual(2, len(related_bands))
        self.assertIn(cassia.slug, related_bands)
        self.assertIn(coldplay.slug, related_bands)

        self.coldplay1['user'] = user_guto
        coldplay = get_or_create_band(self.coldplay1)

        self.assertEqual([beatles.slug, cassia.slug], get_related_bands(band=coldplay))
        self.assertEqual([beatles.slug], get_related_bands(band=coldplay, max=1))

        self.assertEqual([coldplay.slug, cassia.slug], get_related_bands(band=beatles))
        self.assertEqual([coldplay.slug], get_related_bands(band=beatles, max=1))

        related_bands = get_related_bands(band=cassia)
        self.assertEqual(2, len(related_bands))
        self.assertIn(beatles.slug, related_bands)
        self.assertIn(coldplay.slug, related_bands)

        self.assertEqual([], get_related_bands(band=beatles, user=user_guto))

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
        bands = Band.objects.all()
        self.assertEqual(result, None)
        self.assertEqual(len(bands), 0)



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

    def get_or_create_band_with_none_as_user_test(self):
        self.beatles1['user'] = None
        result = get_or_create_band(self.beatles1)
        self.assertEqual(self.beatles1['slug'], result.slug)
        self.assertEqual(self.beatles1['name'], result.name)
        self.assertIn(self.beatles1['name'], result.aliases)
        self.assertEqual(1, len(result.aliases))
        self.assertEqual(0, len(result.users))

    def get_or_create_band_with_musician_test(self):
        """ Teste do fluxo do músico completar o seu cadastro no nosso site """

        user_guilherme = get_or_create_user(data=self.data_user_guilherme)
        user_guto = get_or_create_user(data=self.data_user_guto)
        los_bife = get_or_create_band({"name": "Los Bife", "musician": user_guilherme})
        self.__assert_band__(band=los_bife, slug="los-bife", user=user_guilherme, musician=user_guilherme)
        the_strokes = get_or_create_band({"name": "The Strokes", "musician": user_guilherme, "user": user_guto})
        self.__assert_band__(band=the_strokes, slug="the-strokes", user=user_guto, musician=user_guilherme)
        bands_from_mongo = Band.objects.all()
        self.assertEqual(len(bands_from_mongo), 2)


    def get_or_create_band_passing_only_the_name_test(self):
        band = get_or_create_band({"name": self.beatles1["name"]})
        self.assertEqual(band.name, "The Beatles")
        self.assertEqual(band.slug, "the-beatles")
        self.assertEqual(len(band.aliases), 1)
        self.assertEqual(band.aliases[0], "The Beatles")
        self.assertEqual(len(band.users), 0)


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

    def get_random_bands_from_a_slug_list_test(self):
        slug_list = []
        for i in range(7):
            coldplay_slug = "%s%d" % (self.coldplay1["slug"], i + 1)
            coldplay_name = "%s %d" % (self.coldplay1["name"], i + 1)
            get_or_create_band({"slug": coldplay_slug, "name": coldplay_name})
            if i % 2 == 1:
                slug_list.append(coldplay_slug)

        all_bands = get_all_bands()
        self.assertEqual(len(all_bands), 7)
        bands = get_random_bands_from_a_slug_list(slug_list, max=3)
        self.assertEqual(len(bands), 3)
        for band in bands:
            self.assertIsInstance(band, Band)
            self.assertIn(band.slug, slug_list)
            self.assertIn(band, all_bands)


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

    def get_or_create_newsletter_test(self):
        user_guilherme = get_or_create_user(data=self.data_user_guilherme)
        user_guto = get_or_create_user(data=self.data_user_guto)

        newsletter1 = get_or_create_newsletter(option=False, user=user_guilherme, tipo="Meus Shows")
        self.assertEqual(newsletter1.option, False)

        newsletter2 = get_or_create_newsletter(option=True, user=user_guilherme, tipo="Meus Shows")
        self.assertEqual(newsletter2.option, True)
        self.assertEqual(newsletter1.user, newsletter2.user)

        newsletter3 = get_or_create_newsletter(option=True, user=user_guto, tipo="Meus Shows")
        self.assertNotEqual(newsletter2, newsletter3)
        newsletter4 = get_or_create_newsletter(option=True, user=user_guto, tipo="Shows Locais")
        self.assertNotEqual(newsletter3, newsletter4)

        newsletter_from_mongo = Newsletter.objects.all()
        self.assertEqual(len(newsletter_from_mongo), 3)
        self.assertIn(newsletter3, newsletter_from_mongo)
        newsletter_from_mongo = [n for n in newsletter_from_mongo]
        self.assertEqual(newsletter_from_mongo[0].user.name, "Guilherme")


    def get_or_create_location_test(self):
        maracana = get_or_create_location(self.maracana_data)
        self.assertEqual(maracana.slug, self.maracana_slug)
        locations = Location.objects.all()
        self.assertEqual(len(locations), 1)
        self.assertEqual(maracana, locations[0])

    def get_or_create_show_test(self):
        maracana = get_or_create_location(self.maracana_data)
        show = get_or_create_show({
            'artists': [get_or_create_band(self.beatles1)],
            'attendance_count': 2, #  number of people going
            'cover_image': '', #  Large
            'description': '',
            'datetime_usa': str(datetime.now()), #  From USA datetime to Brazil pattern
            'title': 'beatles show',
            'website': "http://www.beatles.com",
            'location': maracana
        })

        self.__assert_shows__(shows=[show], shows_titles=['Beatles Show'])
        self.assertEqual(show.location, maracana)

        shows = Show.objects.all()
        self.assertEqual(len(shows), 1)

        bands = Band.objects.all()
        self.assertEqual(len(bands), 1)
        self.assertEqual(len(bands[0].shows), 1)

        self.assertEqual(bands[0].shows[0], show)

    def get_shows_from_bands_test(self):
        self.beatles1['user'] = get_or_create_user(data=self.data_user_guilherme)
        beatles = get_or_create_band(self.beatles1)
        self.cassia1['user'] = get_or_create_user(data=self.data_user_guto)
        cassia = get_or_create_band(self.cassia1)

        show1 = get_or_create_show({
            'artists': [beatles, cassia],
            'attendance_count': 2, #  number of people going
            'cover_image': '', #  Large
            'description': '',
            'datetime_usa': str(datetime.now()), #  From USA datetime to Brazil pattern
            'title': 'beatles show',
            'website': "http://www.beatles.com",
            'location': get_or_create_location(self.morumbi_data)
        })

        show2 = get_or_create_show({
            'artists': [cassia],
            'attendance_count': 2, #  number of people going
            'cover_image': '', #  Large
            'description': '',
            'datetime_usa': str(datetime.now()), #  From USA datetime to Brazil pattern
            'title': 'cassia show',
            'website': "http://www.cassia.com",
            'location': get_or_create_location(self.maracana_data)
        })

        bands_shows = get_shows_from_bands(bands=[beatles, cassia], limit_per_artist=1, city="Rio de Janeiro")
        self.assertEqual(len(bands_shows), 2)
        shows_from_mongo = Show.objects.all()
        self.assertEqual(len(shows_from_mongo), 2)

        self.assertEqual(bands_shows[0][0], beatles)
        self.assertEqual(bands_shows[0][1][0], show1)

        self.assertEqual(bands_shows[1][0], cassia)
        self.assertEqual(bands_shows[1][1][0], show2)

    def get_shows_from_bands_force_to_include_band_test(self):
        legiao = get_or_create_band(self.legiao)

        shows = get_shows_from_bands(bands=[legiao], force_to_include_band=False, call_lastfm_if_dont_have_shows=False)
        self.assertEqual(len(shows), 0)

        shows = get_shows_from_bands(bands=[legiao], force_to_include_band=True, call_lastfm_if_dont_have_shows=False)
        self.assertEqual(len(shows), 1)
        self.assertEqual(shows[0][0], legiao)

        show1 = get_or_create_show({
            'artists': [legiao],
            'attendance_count': 2, #  number of people going
            'cover_image': '', #  Large
            'description': '',
            'datetime_usa': "1991-03-20 10:00:00", #  From USA datetime to Brazil pattern
            'title': 'legiao show',
            'website': "http://www.legiaourbana.com.br",
            'location': get_or_create_location(self.morumbi_data)
        })

        shows = get_shows_from_bands(bands=[legiao], force_to_include_band=True, call_lastfm_if_dont_have_shows=False)
        self.assertEqual(len(shows), 1)
        self.assertEqual(shows[0][0], legiao)
        self.assertEqual(shows[0][1][0], show1)


    def get_shows_from_bands_all_in_the_past_test(self):
        self.beatles1['user'] = get_or_create_user(data=self.data_user_guilherme)
        beatles = get_or_create_band(self.beatles1)

        show1 = get_or_create_show({
            'artists': [beatles],
            'attendance_count': 2, #  number of people going
            'cover_image': '', #  Large
            'description': '',
            'datetime_usa': "1991-03-20 10:00:00", #  From USA datetime to Brazil pattern
            'title': 'beatles show',
            'website': "http://www.beatles.com",
            'location': get_or_create_location(self.morumbi_data)
        })

        show2 = get_or_create_show({
            'artists': [beatles],
            'attendance_count': 2, #  number of people going
            'cover_image': '', #  Large
            'description': '',
            'datetime_usa': str(datetime.now()), #  From USA datetime to Brazil pattern
            'title': 'Beatles show 2',
            'website': "http://www.beatles.com",
            'location': get_or_create_location(self.maracana_data)
        })

        shows_from_mongo = Show.objects.all()
        self.assertEqual(len(shows_from_mongo), 2)

        shows = get_shows_from_bands(bands=[beatles], limit_per_artist=None, city=None, call_lastfm_if_dont_have_shows=False)
        self.assertEqual(len(shows), 1)
        self.assertEqual(shows[0][1][0], show2)


    def get_shows_from_bands_by_city_test(self):
        show_initial = get_or_create_show({
            'artists': [get_or_create_band(self.beatles1)],
            'attendance_count': 2, #  number of people going
            'cover_image': '', #  Large
            'description': '',
            'datetime_usa': str(datetime.now()), #  From USA datetime to Brazil pattern
            'title': 'beatles show',
            'website': "http://www.beatles.com",
            'location': get_or_create_location(self.maracana_data)
        })
        self.__assert_shows__(shows=[show_initial], shows_titles=['Beatles Show'])

        shows = get_shows_from_bands_by_city(city=u"Rio de Janeiro")
        shows_from_mongo = Show.objects.all()

        self.assertEqual(len(shows), len(shows_from_mongo))
        self.__assert_shows__(shows_from_mongo, shows_titles=['Beatles Show'])

    def get_shows_from_bands_by_city_with_datetime(self):
        show_initial = get_or_create_show({
            'artists': [get_or_create_band(self.beatles1)],
            'attendance_count': 2, #  number of people going
            'cover_image': '', #  Large
            'description': '',
            'datetime_usa': str(datetime.now()), #  From USA datetime to Brazil pattern
            'title': 'beatles show',
            'website': "http://www.beatles.com",
            'location': get_or_create_location(self.maracana_data)
        })
        shows = get_shows_from_bands_by_city(city=u"Rio de Janeiro", date_to_get=datetime(2013, 5, 13, 14, 30, 45))
        shows_from_mongo = Show.objects.all()
        self.assertEqual(len(shows_from_mongo), 1)

        shows = get_shows_from_bands_by_city(city=u"Rio de Janeiro", date_to_get=datetime(2013, 5, 12, 9, 30, 45))
        self.__assert_shows__(shows, shows_titles=['Beatles Show'])

        shows_from_mongo = Show.objects.all()
        self.assertGreater(len(shows_from_mongo), 1)

    def save_products_test(self):
        product_cd = get_or_create_product(self.product_cd)
        product_camisa = get_or_create_product(self.product_camisa)
        self.coldplay1["products"] = [product_cd, product_camisa]
        get_or_create_band(self.coldplay1)
        bands = get_all_bands()
        products = Product.objects.all()
        self.assertEqual(len(bands), 1)
        self.assertEqual(len(products), 2)
        self.assertIn(product_cd, bands[0].products)
        self.assertIn(product_camisa, bands[0].products)
        products_slugs = [p.slug for p in products]
        products_quantity_lists = [p.quantity_list for p in products]
        self.assertIn("cd-los-bife", products_slugs)
        self.assertIn("camisa-los-bife-amarela", products_slugs)
        self.assertIn(range(1,10,1), products_quantity_lists)
        self.assertIn(['pp', 'p', 'm', 'g'], products_quantity_lists)


    def validate_answers_test(self):
        self.assertFalse(validate_answers(self.invalid_vazio))
        self.assertFalse(validate_answers(self.invalid_musico_fa_vazio))
        self.assertFalse(validate_answers(self.invalid_musico_fa))
        self.assertTrue(validate_answers(self.valid_musico))
        self.assertTrue(validate_answers(self.valid_fa))

    def __assert_question__(self, band_question, band_question_data):
        self.assertEqual(band_question.email, band_question_data["email"])
        self.assertEqual(band_question.question, band_question_data["question"])
        self.assertEqual(band_question.band_slug, band_question_data["band_slug"])

    def __assert_user__(self, user, user_data):
        self.assertEqual(user.facebook_id, user_data["id"])
        self.assertEqual(user.name, user_data["name"])
        self.assertEqual(user.email, user_data["email"])
        if "city" in user_data:
            self.assertEqual(user.city, user_data["city"])
        self.assertEqual(user.photo, 'http://graph.facebook.com/%s/picture' % user_data["id"])

    def __assert_questions__(self, questionsModel, questions):
        for question in questions:
            self.assertIn(question["slug"], [questionModel.slug for questionModel in questionsModel])
