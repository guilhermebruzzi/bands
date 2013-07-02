#!/usr/bin/env python
#-*- coding:utf-8 -*-

from wikipedia import Wikipedia
from wiki2plain import Wiki2Plain

def retira_acentos(st):
    acentos_to_replace = [
        (u'á', u'a'), (u'ã', u'a'), (u'à', u'a'),
        (u'Á', u'a'), (u'Ã', u'a'), (u'À', u'a'),
        (u'é', u'e'), (u'è', u'e'),
        (u'É', u'e'), (u'È', u'e'),
        (u'í', u'i'), (u'ì', u'i'),
        (u'Í', u'i'), (u'Ì', u'i'),
        (u'ó', u'o'), (u'õ', u'o'), (u'ò', u'o'),
        (u'Ó', u'o'), (u'Õ', u'o'), (u'Ò', u'o'),
        (u'ú', u'u'), (u'ù', u'u'),
        (u'Ú', u'u'), (u'Ù', u'u'),
        (u'Ç', u'c'),
        (u'ç', u'c')
    ]

    st = unicode(st, "utf-8")

    for acento_tupla in acentos_to_replace:
        caracter_acento, caracter = acento_tupla
        st = st.replace(caracter_acento, caracter)

    return st

def __get_title(line):
    title = line.strip("= ").lower()
    title = retira_acentos(title)
    return title

def wiki_extract(article, lang='pt'):

    wiki = Wikipedia(lang)
    try:
        raw = wiki.article(article)
    except:
        raw = None

    content = ""

    if raw:
        wiki2plain = Wiki2Plain(raw)
        content = wiki2plain.text

    content_dict = {"resumo": ""}
    current_pointer = content_dict
    parent_pointer = content_dict
    first = True
    for line in content.splitlines():
        line = line.strip()
        if line != "":
            if line.startswith("==") and not line.startswith("==="):
                title = __get_title(line)
                content_dict[title] = {"text": ""}
                parent_pointer = content_dict[title]
                current_pointer = content_dict[title]
                first = False
            elif line.startswith("==="):
                title = __get_title(line)
                parent_pointer[title] = {"text": ""}
                current_pointer = parent_pointer[title]
            else:
                if first:
                    content_dict["resumo"] = "%s<p>%s</p>" % (current_pointer["resumo"], line)
                else:
                    current_pointer["text"] = "%s<p>%s</p>" % (current_pointer["text"], line)


    return content_dict
