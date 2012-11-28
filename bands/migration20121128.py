#!/usr/bin/python
# -*- coding: utf-8 -*-

from models import *
from controllers import get_or_create_question
from config import MAIN_QUESTIONS, QUESTIONS_PESQUISA
from collections import defaultdict

def run_migration():
    users = User.objects.all()
    questions = Question.objects.all()

    user_eh_musico = {
        u"Camille Cardoso": "",
        u"Aline Lucena Nascentes": "",
        u"Bernardo Heynemann": "",
        u"Guto Marrara Marzagao": "",
        u"Guilherme Heynemann Bruzzi": "",
        u"Mariana Marzagao": "",
        u"Irene Heynemann": "",
        u"André Sterenberg Frankenthal": "",
        u"Hélio Cardoso Junior": "",
        u"Michelle Andreu": "",
        u"Pedro Hollanda": "musico",
        u"Rodrigo de Toledo": "fa",
        u"Rafael Lepritiê Werneck": "fa",
        u"Daniel Silli Trevizan": "musico",
        u"Nando Medeiros": "musico",
        u"Eduardo Neves": "",
        u"Guilherme Gualter": "",
    }

    question_slug = {
        u"Quais as suas bandas ou músicos favoritos?": "favoritos",
        u"Quais as suas bandas (ou músicos) favoritas?": "favoritos",
        u"Quais dificuldades você enfrenta na sua banda?": "dificuldades",
        u"Atualmente, como você resolve os problemas que marcou acima?": "solucao",
        u"Quais as funcionalidades mais importantes que você gostaria que tivesse no site?": "funcionalidades",
        u"Que nome para esse produto você gosta mais?": "nome"
    }
    slug_answers = defaultdict(list)

    for question in questions:
        if question.question == u"Você é músico?":
           for answer in question.answers:
               if answer.answer == "musico":
                   user_eh_musico[answer.user.name] = "musico"
               else:
                   user_eh_musico[answer.user.name] = "fa"

    import ipdb; ipdb.set_trace()

    for question in questions:
        if question.question == u"Você é músico?":
            continue

        for answer in question.answers:
            user = answer.user
            slug = "%s-%s" % (user_eh_musico[user.name], question_slug[question.question])
            slug_answers[slug].append(answer)

#    question_main = get_or_create_question({"question": u"Você é músico?", "slug": "musico-ou-fa"} )
#    answers_main = []
#    for user_name, answer in user_eh_musico.items():
#        for user in users:
#            if user.name == user_name:
#                answer_instance = Answer(answer=answer, user=user)
#                answers_main.append(answer_instance)
#    question_main.answers = answers_main
#    question_main.save()
#
#    for question_pesquisa in QUESTIONS_PESQUISA:
#        slug = question_pesquisa["slug"]
#        question = get_or_create_question({"question": question_pesquisa["question"], "slug": slug})
#        question.answers = slug_answers[slug]
#        question.save()
