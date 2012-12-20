#!/usr/bin/python
# -*- coding: utf-8 -*-

from bands.controllers import get_musicians_from_opengraph, get_or_create_band
from bands.models import User

def run_migration():
    oauth_token = "AAAEGO5mvMs0BALaWzyeh7HiL2aruu2Uxu5oS0gISC4hnD8VHkG05ZAH5fYzCBbnOCsEkZBLI7glTMY6iR3N0BC9i7TXyFqH1uCVW0RNQZDZD"
    users = User.objects.all()
    for user in users:
        import ipdb; ipdb.set_trace()
        bands_facebook = get_musicians_from_opengraph(user.facebook_id, oauth_token)
        for band_facebook in bands_facebook:
            get_or_create_band({"slug": band_facebook, "name": band_facebook, "user": user})
