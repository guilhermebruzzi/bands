#-*- coding:utf-8 -*-

from mongoengine.queryset import DoesNotExist
from models import User, Question, Answer
from config import QUESTIONS_PESQUISA


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


def get_question(question_text):
    return Question.objects.filter(question=question_text).first()



def get_all_answers_from_question(question_text):
    question = get_question(question_text)
    return question.answers


def __sort_and_make_unique_answers__(answers_instances):
    answers = [answer.answer for answer in answers_instances]
    answers = list(set(answers))
    answers = sorted(answers)
    return answers


def get_questions_and_all_answers():
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
    if "answer_main" in data.keys() and (data["answer_main"] == "musico" or data["answer_main"] == "fa"):
        return True

    return False


def __create_list_of_answers_for_a_question__(key, data, user, answers_original):
    answers = []
    if key in data.keys():
        data_answers = data[key]

        if not type(data_answers) is list:
            data_answers = [data_answers]

        for answer in data_answers:
            if answer != "":
                answer_instance = Answer(answer=answer, user=user)
                if not answer_instance in answers_original:
                    answers.append(answer_instance)

    return answers


def __save_answer_main__(data, current_user):
    question_main = get_or_create_questions([u"Você é músico?"])[0]

    answer_main = __create_list_of_answers_for_a_question__(key="answer_main", data=data,
        user=current_user, answers_original=question_main.answers)

    question_main.answers.extend(answer_main)

    question_main.save()


def save_answers(data, current_user):
    __save_answer_main__(data, current_user)

    question_index = 0

    questions = get_or_create_questions([question["question"] for question in QUESTIONS_PESQUISA if question["class_name"] == data["answer_main"]])

    for question_pesquisa_index in range(len(QUESTIONS_PESQUISA)):

        if QUESTIONS_PESQUISA[question_pesquisa_index]["class_name"] == data["answer_main"]:

            answers_created = __create_list_of_answers_for_a_question__(key="answers%d" % question_pesquisa_index, data=data,
                user=current_user, answers_original=questions[question_index].answers)

            questions[question_index].answers.extend(answers_created)

            answers_outros_created = __create_list_of_answers_for_a_question__(key="answers_outros%d" % question_pesquisa_index, data=data,
                user=current_user, answers_original=questions[question_index].answers)

            questions[question_index].answers.extend(answers_outros_created)

            questions[question_index].save()

            question_index += 1
