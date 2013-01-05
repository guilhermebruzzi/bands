from helpers import get_json

def get_musicians_from_opengraph(facebook_id, oauth_token):
    url_to_get_musicians = "https://graph.facebook.com/%s/music?access_token=%s" % (facebook_id, oauth_token)
    musicians = get_json(url_to_get_musicians)

    musicians_names = []
    if "data" in musicians.keys():
        while len(musicians["data"]) > 0:
            for music in musicians["data"]:
                if music["category"] == "Musician/band":
                    musicians_names.append(music["name"])

            if "paging" in musicians.keys() and "next" in musicians["paging"].keys():
                musicians = get_json(musicians["paging"]["next"])
            else:
                break

    return musicians_names