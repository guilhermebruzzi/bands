#!/usr/bin/env python
#-*- coding:utf-8 -*-

import pylast
from datetime import datetime

from controllers import get_or_create_band

# You have to have your own unique two values for API_KEY and API_SECRET
# Obtain yours from http://www.last.fm/api/account for Last.fm
API_KEY = "13a9fd8318ec83d2cac2797d23005daa"
API_SECRET = "d639fb1b527f4bb6aabe57bd3aa77205"

network = pylast.LastFMNetwork(api_key=API_KEY, api_secret=API_SECRET)

def get_show_info(show):
    """ show: event from lastfm. Get all info from that show. """
    show_datetime = datetime.strptime(show.get_start_date(), '%a, %d %b %Y %H:%M:%S') #  From USA pattern to datetime
    return {
            'artists': [get_or_create_band({"name": artist.get_name()}) for artist in show.get_artists()],
            'attendance_count': show.get_attendance_count(), #  number of people going
            'cover_image': show.get_cover_image(),
            'description': show.get_description(),
            'data': datetime.strftime(show_datetime, '%d/%m/%Y %H:%M:%S'), #  From USA datetime to Brazil pattern
            'title': show.get_title(),
    }

def get_next_shows(artists, limit_per_artist=None):
    events = []
    for artist in artists:
        artist_lastfm = network.get_artist(artist)
        events_lastfm = artist_lastfm.get_upcoming_events()[:limit_per_artist]
        for event in events_lastfm:
            try:
                events.append((artist, get_show_info(event)))
            except pylast.WSError as e: #  Ignora eventos que não conseguiu pegar as informações
                continue
    return events
