#-*- coding:utf-8 -*-

from mongoengine.queryset import DoesNotExist
from models import User, Question, Answer
from config import QUESTIONS_PESQUISA, MAIN_QUESTIONS


def get_or_create_user(data):
    try:
        user = User.objects.get(facebook_id=data['id'])
    except DoesNotExist:
        user = User.objects.create(facebook_id=data['id'], email=data['email'], name=data['name'])
    return user


def get_or_create_questions(questions_data):
    questions = []
    for question_data in questions_data:
        try:
            question = Question.objects.get(slug=question_data["slug"])
            if question.question != question_data["question"]:
                question.question = question_data["question"]
                question.save()
        except DoesNotExist:
            question = Question.objects.create(slug=question_data["slug"], question=question_data["question"])
        questions.append(question)
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
    questions_and_all_answers = []
    questions_text = []

    question_main_text = u"Você é músico?"
    answers_main = __sort_and_make_unique_answers__(answers_instances=get_all_answers_from_question(question_main_text))
    questions_and_all_answers.append({"question": question_main_text, "answers": answers_main})

    for question_pesquisa in QUESTIONS_PESQUISA:
        question_text = question_pesquisa["question"]
        if not question_text in questions_text:
            questions_text.append(question_text)
            answers = __sort_and_make_unique_answers__(answers_instances=get_all_answers_from_question(question_text))
            questions_and_all_answers.append({"question": question_text, "answers": answers})
    return questions_and_all_answers


def validate_answers(data):
    if "musico-ou-fa" in data.keys() and (data["musico-ou-fa"] == "musico" or data["musico-ou-fa"] == "fa"):
        return True

    return False


def __create_answers_for_question__(question, answers, user):
    if not type(answers) is list:
        answers = [answers]

    for answer in answers:
        if answer != "":
            answer_instance = Answer(answer=answer, user=user)
            if not answer_instance in question.answers:
                question.answers.append(answer_instance)

    question.save()


def save_answers(data, current_user):
    questions = get_or_create_questions(MAIN_QUESTIONS)
    questions.extend(get_or_create_questions(QUESTIONS_PESQUISA))

    for question in questions:
        if question.slug in data.keys():
            __create_answers_for_question__(question=question, answers=data[question.slug], user=current_user)

        key = "%s%s" % (question.slug, "_outros")
        if key in data.keys():
            __create_answers_for_question__(question=question, answers=data[key], user=current_user)
