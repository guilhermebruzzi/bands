#-*- coding:utf-8 -*-

import random

from mongoengine.queryset import DoesNotExist
from models import User, Question, Answer
from config import QUESTIONS_PESQUISA, MAIN_QUESTIONS


def get_or_create_user(data):
    try:
        user = User.objects.get(facebook_id=data['id'])
    except DoesNotExist:
        user = User.objects.create(facebook_id=data['id'], email=data['email'], name=data['name'])
    return user

def get_random_users(max=8):
    users = User.objects.all()
    users_random = []
    if users:
        for repeat in range(max):
            user_random = random.choice(users)
            user_random.name = user_random.name.split(" ")[0]
            users_random.append(user_random)
    return (users_random, len(users))


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


def __sort_and_make_unique_answers__(answers_instances):
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


def save_answers(data, current_user):
    for key, value in data.items():
        for i in range(len(value)):
            if value[i] == "":
                del value[i]
        if len(value) == 0:
            del data[key]

    for question in MAIN_QUESTIONS:
        __save_question_answers__(question, data, current_user)

    for question in QUESTIONS_PESQUISA:
        __save_question_answers__(question, data, current_user)
