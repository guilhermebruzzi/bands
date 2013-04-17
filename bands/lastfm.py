#!/usr/bin/env python
#-*- coding:utf-8 -*-

import urllib
from datetime import datetime
from multiprocessing import Process

import pylast
import mongoengine

from helpers import get_json
from controllers import get_or_create_band, get_or_create_show, get_or_create_location

# You have to have your own unique two values for API_KEY and API_SECRET
# Obtain yours from http://www.last.fm/api/account for Last.fm
API_KEY = "13a9fd8318ec83d2cac2797d23005daa"
API_SECRET = "d639fb1b527f4bb6aabe57bd3aa77205"

network = pylast.LastFMNetwork(api_key=API_KEY, api_secret=API_SECRET)

def __get_shows__(url_shows):
    response_lastfm = get_json(url_shows)
    shows_json = response_lastfm["events"]["event"] if "events" in response_lastfm and "event" in response_lastfm["events"] else []
    shows = []
    if not type(shows_json) is list:
        shows_json = [shows_json]
    
    for show_json in shows_json:
        try:
            artists = show_json['artists']['artist']
        except TypeError as e:
            print e
            print show_json
            continue
        if not type(artists) is list:
            artists = [artists]
        show_datetime = datetime.strptime(show_json['startDate'], '%a, %d %b %Y %H:%M:%S') #  From USA pattern to datetime
        show =  get_or_create_show({
            'artists': [get_or_create_band({'name': artist}) for artist in artists],
            'attendance_count': show_json['attendance'], #  number of people going
            'cover_image': show_json['image'][2]['#text'], #  Large
            'description': show_json['description'],
            'datetime_usa': datetime.strftime(show_datetime, '%Y-%m-%d %H:%M:%S'), #  From datetime to string
            'title': show_json['title'],
            'website': show_json['website'],
            'location': get_or_create_location({
                'name': show_json['venue']['name'],
                'city': show_json['venue']['location']['city'],
                'street': show_json['venue']['location']['street'],
                'postalcode': show_json['venue']['location']['postalcode'],
                'website': show_json['venue']['website'],
                'phonenumber': show_json['venue']['phonenumber'],
                'image': show_json["image"][2]["#text"], #  Large
            })
        })
        if not show in shows:
            shows.append(show)
#    TODO: Logging de warning - if len(shows) == 0 :
#        print url_shows
    return shows

def get_nearby_shows(city):
    params = {"method": "geo.getevents", "location": city, "api_key": network.api_key, "format": "json"}
    url = 'http://ws.audioscrobbler.com/2.0/?%s' % urllib.urlencode(params)
    return __get_shows__(url)

def save_next_shows(bands):
    for band in bands:
        try:
            params = {"method": "artist.getevents", "artist": band.name, "autocorrect": '1', "api_key": network.api_key, "format": "json"}
            params = urllib.urlencode(dict([k, v.encode('utf-8')] for k, v in params.items()))
            url = 'http://ws.audioscrobbler.com/2.0/?%s' % params
        except UnicodeEncodeError as e:
            print e
            print params
        return __get_shows__(url)

def get_photo_from_band(band):
    params = {"method": "artist.getinfo", "artist": band.name, "autocorrect": '1', "api_key": network.api_key, "format": "json"}
    params = urllib.urlencode(dict([k, v.encode('utf-8')] for k, v in params.items()))
    url = 'http://ws.audioscrobbler.com/2.0/?%s' % params
    response_lastfm = get_json(url)
    return response_lastfm["artist"]["image"][3]['#text']


def get_next_shows_subprocess(bands):
    p = Process(target=save_next_shows, args=(bands,))
    p.start()
