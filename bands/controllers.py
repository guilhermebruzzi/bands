#-*- coding:utf-8 -*-

import random
from operator import itemgetter

from mongoengine.queryset import DoesNotExist, MultipleObjectsReturned

from models import User, Question, Answer, Band, Show, Location
from config import QUESTIONS_PESQUISA, MAIN_QUESTIONS
from helpers import get_slug
from facebook import get_musicians_from_opengraph

lastfm = None

def get_lastfm_module():
    global lastfm
    if lastfm is None:
        lastfm = __import__("lastfm")
    return lastfm

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

def get_all_users():
    return User.objects.order_by('-name')

def get_user_answers(user):
    answers_from_user = []
    questions = Question.objects.all()
    for question in questions:
        for answer in question.answers:
            if answer.user == user:
                answers_from_user.append(answer)
    return answers_from_user

def get_or_create_band(data):
    name = data['name'].title()
    slug = get_slug(data['slug']) if "slug" in data else get_slug(data['name'])
    try:
        band = Band.objects.get(slug=slug)
    except DoesNotExist:
        band = Band.objects.create(slug=slug, name=name)

    if not name in band.aliases:
        band.aliases.append(name)

    if "user" in data and not data['user'] in band.users:
        band.users.append(data['user'])

    band.save()
    return band

def get_or_create_location(data):
    slug = get_slug(data['slug']) if "slug" in data else get_slug(data['name'])
    try:
        location = Location.objects.get(slug=slug)
    except DoesNotExist:
        data["slug"] = slug
        location = Location.objects.create(**data)

    return location

def get_or_create_show(data):
    title = data['title'].title()
    slug = get_slug(data['slug']) if "slug" in data else get_slug(data['title'])
    try:
        show = Show.objects.get(slug=slug)
    except DoesNotExist:
        show = Show.objects.create(slug=slug, title=title)

    if "artists" in data and type(data["artists"]) is list:
        for artist in data["artists"]:
            if not artist.slug in show.artists_slug:
                show.artists_slug.append(artist.slug)

    if "location" in data:
        show.location = get_or_create_location(data["location"])

    keys_to_check = ["attendance_count", "cover_image", "description", "datetime", "city"]
    for key in keys_to_check:
        if key in data:
            setattr(show, key, data[key])

    show.save()
    return show

def get_shows_from_bands(bands):
    shows = []
    for band in bands:
        if len(bands.shows) == 0:
            lastfm = get_lastfm_module()
            lastfm.get_next_shows_subprocess(bands)
        else:
            shows.extend(band.shows)
    return shows

def get_shows_from_bands_by_city(city):
    return Show.objects.filter(city=city)


def get_band(slug):
    return Band.objects.filter(slug=slug).first()

def get_related_bands(band, max=None, user=None):
    bands = Band.objects.all()
    related_bands = {}
    for currentUser in band.users:
        for currentBand in bands:
            if currentUser in currentBand.users and currentBand != band and \
                    (user is None or not user in currentBand.users):
                if currentBand.slug in related_bands:
                    related_bands[currentBand.slug] += 1
                else:
                    related_bands[currentBand.slug] = 1

    list = related_bands.items()
    random.shuffle(list)
    list.sort(key=lambda tup: tup[1], reverse=True)

    slugs = []
    for tuple in list:
        slug, weight = tuple
        slugs.append(slug)

    return slugs[0:max]

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

    if len(band.users) == 0:
        band.delete()

    band.save()

def get_top_bands(max=None, sort=False, normalize=False, maxSize=6):
    bands = Band.objects.all()
    top_bands = []
    top_band_size = 0;

    for band in bands:
        top_bands.append({"label": band.name, "size": len(band.users)})
        if len(band.users) > top_band_size:
            top_band_size = len(band.users)

    result = sorted(top_bands, key=itemgetter('size'), reverse=True)
    result = result[0:max]

    if normalize and top_band_size != 0:
        for band in result:
            band["size"] = int((maxSize * band["size"]) / top_band_size)

    if not sort:
        random.shuffle(result)

    return (result, len(bands))


def random_top_bands(max=None, user=None): #  Sorteia bandas baseado na quantidade de votos dela
    bands = Band.objects.all()
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
        if "question" in question_data.keys() and question.question != question_data["question"]:
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

def get_answers_and_counters_from_question(slugs):
    answers = []

    for slug in slugs:
        answers.extend(get_all_answers_from_question(slug))

    parcial = {}
    for answer in answers:
        if answer.answer in parcial.keys():
            parcial[answer.answer] += 1
        else:
            parcial[answer.answer] = 1

    resultado = parcial.items()
    return sorted(resultado, key=lambda tup: tup[1], reverse=True)

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
        questions_and_answers[question.slug] = {"question": question, "answers": answers}

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
