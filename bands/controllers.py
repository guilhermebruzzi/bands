#-*- coding:utf-8 -*-

from mongoengine.queryset import DoesNotExist
from models import User, Question


def get_or_create_user(data):
    try:
        user = User.objects.get(facebook_id=data['id'])
    except DoesNotExist:
        user = User.objects.create(facebook_id=data['id'], email=data['email'], name=data['name'])
    return user


def get_or_create_questions(questions_text):
    questions = []
    for question_text in questions_text:
        question, created = Question.objects.get_or_create(question=question_text)
        questions.append(question)
    return questions


def get_all_answer_from_question(question_text):
    return Question.objects.filter(question=question_text).answers

def get_question(question_text):
    pass

def validate_answers(data):
    pass

def create_answers(data):
    pass
    #Para cada pergunta em data (dicionario com o que foi preenchido no formulario)
    # current_user = session["current_user"]
    # get_question(pergunta)
    # Para cada resposta dessa pergunta, inserir essa resposta




