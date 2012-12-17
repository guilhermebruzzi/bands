#-*- coding:utf-8 -*-

import random

from mongoengine.queryset import DoesNotExist
from models import User, Question, Answer, Band
from config import QUESTIONS_PESQUISA, MAIN_QUESTIONS
from helpers import get_musicians_from_opengraph, get_slug
from operator import itemgetter

def get_or_create_user(data, oauth_token=None):
    try:
        user = User.objects.get(facebook_id=data['id'])
    except DoesNotExist:
        # Ao criar um usuário do facebook, eu importo as bandas favoritas dele
        user = User.objects.create(facebook_id=data['id'], email=data['email'], name=data['name'])
        if oauth_token: #  Se foi passado, é para buscar as bandas no facebook
            bands_facebook = get_musicians_from_opengraph(user.facebook_id, oauth_token)
            for band_facebook in bands_facebook:
                get_or_create_band({"slug": band_facebook, "name": band_facebook, "user": user})
    return user

def get_or_create_band(data):
    slug = get_slug(data['slug'])
    try:
        band = Band.objects.get(slug=slug)
    except DoesNotExist:
        band = Band.objects.create(slug=slug, name=data['name'])

    if not data['name'] in band.aliases:
        band.aliases.append(data['name'])

    if not data['user'] in band.users:
        band.users.append(data['user'])

    band.save()
    return band

def get_band(slug):
    return Band.objects.filter(slug=slug).first()

def like_band(slug, user):
    band = get_band(slug)

    if not user in band.users:
        band.users.append(user)

    band.save()

def unlike_band(slug, user):
    band = get_band(slug)

    for i in range(len(band.users)):
        if band.users[i] == user:
            del band.users[i]
            break

    band.save()

def get_top_bands(max=None):
    bands = Band.objects.all()
    if max == None:
        max = len(bands)
        if max == 0:
            return []

    top_bands = []

    for band in bands:
        top_bands.append({"label": band.name, "size": len(band.users)})

    result = sorted(top_bands, key=itemgetter('size'), reverse=True)

    return (result[0:max], len(bands))


def random_top_bands(max=None, user=None): #  Sorteia bandas baseado na quantidade de votos dela
    bands = Band.objects.all()
    if max == None:
        max = len(bands)
        if max == 0:
            return []

    removidos = {}
    bandas = []
    for band in bands:
        if not user or not user in band.users:
            for u in band.users:
                bandas.append(band)
                removidos[band.slug] = False

    bandasOrdenadas = []
    while len(bandas) > 0:
        tamanho = len(bandas)
        indice = random.randint(0, tamanho - 1)
        if not removidos[bandas[indice].slug]:
            bandasOrdenadas.append(bandas[indice])
            removidos[bandas[indice].slug] = True
        del bandas[indice]

    return bandasOrdenadas[0:max]

def get_user_bands(user):
    bands = Band.objects.all()
    return [band for band in bands if user in band.users]

def get_random_users(max=8):
    users = [user for user in User.objects.all()]
    users_random = set()
    len_users = 0
    if users:
        len_users = len(users)
        if max >= len_users:
            for user_index in range(len(users)):
                users[user_index].name = users[user_index].name.split(" ")[0]
            return (users, len_users)

        for i in range(max): # repete max vezes
            choice = random.choice(range(len(users)))
            user_random = users[choice]
            user_random.name = user_random.name.split(" ")[0]
            users_random.add(user_random)
            del users[choice]

    return (list(users_random), len_users)


def get_or_create_question(question_data):
    try:
        question = Question.objects.get(slug=question_data["slug"])
        if question.question != question_data["question"]:
            question.question = question_data["question"]
            question.save()
        return question
    except DoesNotExist:
        question = Question.objects.create(slug=question_data["slug"], question=question_data["question"])
        return question


def get_or_create_questions(questions_data):
    questions = []
    for question_data in questions_data:
        questions.append(get_or_create_question(question_data))
    return questions


def get_question(slug):
    return Question.objects.filter(slug=slug).first()


def get_all_answers_from_question(slug, user=None):
    question = get_question(slug)
    if question:
        answers = question.answers
        if user:
            answers = [answer for answer in answers if answer.user==user]
        return answers
    return []


def sort_and_make_unique_answers(answers_instances):
    answers = [answer.answer for answer in answers_instances]
    answers = list(set(answers))
    answers = sorted(answers)
    return answers


def get_all_questions_and_all_answers():
    questions_and_answers = {}
    questions = Question.objects.all()

    for question in questions:
        answers = []
        for answer in question.answers:
            answers.append(answer.answer)
        questions_and_answers[question.slug] = answers

    return questions_and_answers


def validate_answers(data):
    if "musico-ou-fa" in data.keys() and (data["musico-ou-fa"] == ["musico"] or data["musico-ou-fa"] == ["fa"]):
        return True

    return False


def __create_answers_for_question__(question, answers, user):
    questionModel = get_or_create_question(question)

    if not type(answers) is list:
        answers = [answers]

    for answer in answers:
        if answer != "":
            answer_instance = Answer(answer=answer, user=user)
            if not answer_instance in questionModel.answers:
                questionModel.answers.append(answer_instance)

    questionModel.save()


def __save_question_answers__(question, data, current_user):
    if question["slug"] in data.keys():
        __create_answers_for_question__(question=question, answers=data[question["slug"]], user=current_user)

    key = "%s%s" % (question["slug"], "_outros")
    if key in data.keys():
        __create_answers_for_question__(question=question, answers=data[key], user=current_user)


def save_answers(data, current_user, *questions_lists):
    for key, value in data.items():
        for i in range(len(value)):
            if value[i] == "":
                del value[i]
        if len(value) == 0:
            del data[key]

    if len(questions_lists) == 0:
        questions_lists = []
        questions_lists.append(MAIN_QUESTIONS)
        questions_lists.append(QUESTIONS_PESQUISA)

    for questions_list in questions_lists:
        for question in questions_list:
            __save_question_answers__(question, data, current_user)
