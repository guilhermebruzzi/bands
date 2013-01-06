#!/usr/bin/env python
#-*- coding:utf-8 -*-

import re
import urllib
from datetime import datetime
from multiprocessing import Process

import pylast

from controllers import get_or_create_band, get_or_create_show, get_or_create_location

# You have to have your own unique two values for API_KEY and API_SECRET
# Obtain yours from http://www.last.fm/api/account for Last.fm
API_KEY = "13a9fd8318ec83d2cac2797d23005daa"
API_SECRET = "d639fb1b527f4bb6aabe57bd3aa77205"

network = pylast.LastFMNetwork(api_key=API_KEY, api_secret=API_SECRET)

def __get_tag_value__(xml, tag_name, property_of_tag=""):
    pre, post = '<%s%s>' % (tag_name, property_of_tag), '</%s>' % tag_name
    regex = re.compile(pre + '.*' + post)
    match = regex.search(xml).group()
    return match[len(pre) : 0 - len(post)]

def get_location_info(show):
    show_id = str(show.get_id())
    url = 'http://ws.audioscrobbler.com/2.0/?method=event.getinfo&event='
    url += show_id
    url += '&api_key='
    url += show.network.api_key
    show_xml = urllib.urlopen(url).read()
    return get_or_create_location({
        'name': __get_tag_value__(show_xml, 'name'),
        'city': __get_tag_value__(show_xml, 'city'),
        'street': __get_tag_value__(show_xml, 'street'),
        'postalcode': __get_tag_value__(show_xml, 'postalcode'),
        'website': __get_tag_value__(show_xml, 'website'),
        'phonenumber': __get_tag_value__(show_xml, 'phonenumber'),
        'image': __get_tag_value__(show_xml, 'image', property_of_tag=' size="large"'),
    })

def save_show_info(show):
    """ show: event from lastfm. Get all info from that show. """

    show_datetime = datetime.strptime(show.get_start_date(), '%a, %d %b %Y %H:%M:%S') #  From USA pattern to datetime

    return get_or_create_show({
        'artists': [get_or_create_band({"name": artist.get_name()}) for artist in show.get_artists()],
        'attendance_count': show.get_attendance_count(), #  number of people going
        'cover_image': show.get_cover_image(),
        'description': show.get_description(),
        'datetime': datetime.strftime(show_datetime, '%d/%m/%Y %H:%M:%S'), #  From USA datetime to Brazil pattern
        'title': show.get_title(),
        'location': get_location_info(show)
    })

def save_next_shows(artists, limit_per_artist=None):
    for artist in artists:
        artist_lastfm = network.get_artist(artist)
        events_lastfm = artist_lastfm.get_upcoming_events()[:limit_per_artist]
        for event in events_lastfm:
            try:
                save_show_info(event)
            except pylast.WSError as e: #  Ignora eventos que não conseguiu pegar as informações
                continue


def get_next_shows_subprocess(artists, limit_per_artist=None):
    p = Process(target=save_next_shows, args=(artists, limit_per_artist))
    p.start()
