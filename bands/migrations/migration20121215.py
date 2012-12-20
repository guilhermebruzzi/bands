#!/usr/bin/python
# -*- coding: utf-8 -*-

from controllers import get_or_create_band, get_all_answers_from_question
from helpers import get_slug

def run_migration():
    answers = get_all_answers_from_question("musico-favoritos")
    answers.extend(get_all_answers_from_question("fa-favoritos"))

    for answer in answers:
        bandsList = answer.answer
        for bands in bandsList.split(","):
            for splited in bands.split('\n'):
                band = splited.strip().title()
                if band:
                    data = {
                        "slug": get_slug(band),
                        "name": band,
                        "user": answer.user
                    }

                    get_or_create_band(data)
