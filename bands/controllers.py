#-*- coding:utf-8 -*-

from datetime import datetime
import random
from operator import itemgetter

from mongoengine.queryset import DoesNotExist, MultipleObjectsReturned

from models import User, Question, Band, Show, Location, Newsletter, Product, BandQuestion
from helpers import get_slug
from facebook import get_musicians_from_opengraph

lastfm = None

def get_lastfm_module():
    global lastfm
    if lastfm is None:
        lastfm = __import__("lastfm")
    return lastfm

def get_or_create_band_question(data):
    try:
        band_question = BandQuestion.objects.get(email=data['email'], question=data['question'], band_slug=data["band_slug"])
    except DoesNotExist:
        band_question = BandQuestion.objects.create(email=data['email'], question=data['question'], band_slug=data["band_slug"])

    return band_question

def get_or_create_user(data, oauth_token=None):
    try:
        user = User.objects.get(facebook_id=data['id'])
    except DoesNotExist:
        # Ao criar um usuário do facebook, eu importo as bandas favoritas dele
        user = User.objects.create(facebook_id=data['id'], email=data['email'], name=data['name'])
        if oauth_token: #  Se foi passado, é para buscar as bandas no facebook
            bands_facebook = get_musicians_from_opengraph(user.facebook_id, oauth_token)
            for band_facebook in bands_facebook:
                get_or_create_band({"slug": band_facebook, "name": band_facebook, "user": user})

    if "city" in data and data['city'] and data['city'] != user.city:
        user.city = data['city']
        user.save()

    return user

def get_all_users():
    return User.objects.order_by('-name')

def newsletter_exists(tipo, user):
    try:
        newsletter = Newsletter.objects.get(user=user, tipo=tipo)
        return True
    except DoesNotExist:
        return False

def get_or_create_newsletter(tipo, user, option=None):
    try:
        newsletter = Newsletter.objects.get(user=user, tipo=tipo)
        if option:
            newsletter.option = option
            newsletter.save()
    except DoesNotExist:
        newsletter = Newsletter.objects.create(user=user, option=option, tipo=tipo)

    return newsletter

def get_all_newsletters():
    return Newsletter.objects.all()


def get_or_create_band(data):
    name = data['name'].title()
    slug = get_slug(data['slug']) if "slug" in data else get_slug(data['name'])
    try:
        band = Band.objects.get(slug=slug)
    except DoesNotExist:
        band = Band.objects.create(slug=slug, name=name)

    if not name in band.aliases:
        band.aliases.append(name)

    if "musician" in data and data['musician'] and not data['musician'] in band.musicians:
        band.musicians.append(data['musician'])
        if not "user" in data:
            band.users.append(data['musician'])
        else:
            if data['musician'] != data['user']:
                band.users.append(data['musician'])

    if "user" in data and data['user'] and not data['user'] in band.users:
        band.users.append(data['user'])

    if "image" in data and data['image']:
        band.image = data['image']

    if "products" in data and data["products"]:
        for product in data["products"]:
            if not product in band.products:
                band.products.append(product)

    band.save()
    return band

def get_or_create_location(data):
    try:
        slug = get_slug(data['slug']) if "slug" in data else get_slug(data['name'])
    except UnicodeDecodeError:
        slug = data['name']
    try:
        location = Location.objects.get(slug=slug)
    except DoesNotExist:
        data["slug"] = slug
        location = Location.objects.create(**data)

    return location

def get_or_create_show(data):
    title = data['title'].title()
    slug = get_slug(data['slug']) if "slug" in data else get_slug(data['title'])
    try:
        show = Show.objects.get(slug=slug)
    except DoesNotExist:
        show = Show.objects.create(slug=slug, title=title)

    if "artists" in data and type(data["artists"]) is list:
        for artist in data["artists"]:
            if not artist.slug in show.artists_slug:
                show.artists_slug.append(artist.slug)
                if not show in artist.shows:
                    artist.shows.append(show)
                    artist.save()

    if "location" in data:
        if isinstance(data["location"], Location): #  Um objeto location tambem pode ter sido passado
            show.location = data["location"]
        else:
            show.location = get_or_create_location(data["location"])

    keys_to_check = ["attendance_count", "cover_image", "description", "datetime_usa", "city", "website"]
    for key in keys_to_check:
        if key in data:
            setattr(show, key, data[key])

    show.save()
    return show

def __sort_by_city_and_date__(city=None):
    now = str(datetime.now())

    if city:
        return lambda show: ("0" + show.datetime_usa if show.location.city == city else show.datetime_usa) if show.datetime_usa[:10] >= now[:10] else ("9" + show.datetime_usa)

    return lambda show: show.datetime_usa if show.datetime_usa[:10] >= now[:10] else "9" + show.datetime_usa

def __add_to_bands_to_get_shows__(band, shows, bands_to_get_shows, limit_per_artist, force_to_include_band):
    if force_to_include_band:
        if not hasattr(band, "shows") or len(band.shows) == 0:
            shows.append((band, []))
        else:
            shows.append((band, band.shows[:limit_per_artist]))
    bands_to_get_shows.append(band)

def get_shows_from_bands(bands, limit_per_artist=None, city=None, force_to_include_band=False, call_lastfm_if_dont_have_shows=True, call_lastfm_without_subprocess=False):
    """ bands: Uma lista de bandas nas quais pegará os limit_per_artist shows (default: None = todos os shows) e ordenará por city se for passado algo """

    shows = []
    bands_to_get_shows = []
    for band in bands:
        if not band:
            continue
        if hasattr(band, "shows") and len(band.shows) == 0:
            __add_to_bands_to_get_shows__(band, shows, bands_to_get_shows, limit_per_artist, force_to_include_band)
        else:
            band.shows = sorted(band.shows, key=__sort_by_city_and_date__(city=city))
            if band.shows[0].datetime_usa[:10] < str(datetime.now())[:10]: #  Se o primeiro show já aconteceu, quer dizer que todos já aconteceram, nesse caso, pega mais do lastfm
                __add_to_bands_to_get_shows__(band, shows, bands_to_get_shows, limit_per_artist, force_to_include_band)
            else:
                shows.append((band, band.shows[:limit_per_artist]))
    if call_lastfm_if_dont_have_shows and len(bands_to_get_shows) > 0:
        lastfm = get_lastfm_module()
        if call_lastfm_without_subprocess:
            shows_to_get = lastfm.save_next_shows(bands_to_get_shows)
            for show in shows_to_get:
                band = show.artists[0]
                shows.append((band, band.shows[:limit_per_artist]))
        else:
            lastfm.get_next_shows_subprocess(bands_to_get_shows)
    return shows

def get_shows_from_bands_by_city(city, date_to_get=None):
    shows = []

    if not date_to_get:
        date_to_get = datetime.now()

    if int(date_to_get.strftime("%w")) == 0 and int(date_to_get.strftime("%H")) >= 0 and int(date_to_get.strftime("%H")) <= 11:
        lastfm = get_lastfm_module()
        shows = lastfm.get_nearby_shows(city=city)

    locations = Location.objects.filter(city=city)
    shows_from_mongo = Show.objects.filter(location__in=locations, datetime_usa__gte=str(datetime.now().date()))
    for show_mongo in shows_from_mongo:
        if not show_mongo in shows:
            shows.append(show_mongo)

    shows = sorted(shows, key=__sort_by_city_and_date__(city=city))

    return shows

def get_all_bands(limit=None):
    if limit:
        return Band.objects[:limit].order_by("-users")
    return Band.objects.order_by("-users")

def get_band(slug):
    return Band.objects.filter(slug=slug).first()



def get_related_bands(band, max=None, user=None):
    bands = get_all_bands()
    related_bands = {}
    for currentUser in band.users:
        for currentBand in bands:
            if currentUser in currentBand.users and currentBand != band and \
                    (user is None or not user in currentBand.users):
                if currentBand.slug in related_bands:
                    related_bands[currentBand.slug] += 1
                else:
                    related_bands[currentBand.slug] = 1

    list = related_bands.items()
    random.shuffle(list)
    list.sort(key=lambda tup: tup[1], reverse=True)

    slugs = []
    for tuple in list:
        slug, weight = tuple
        slugs.append(slug)

    return slugs[0:max]

def like_band(slug, user):
    band = get_band(slug)

    if not user in band.users:
        band.users.append(user)

    band.save()

def unlike_band(slug, user):
    band = get_band(slug)

    for i in range(len(band.users)):
        if band.users[i] == user:
            del band.users[i]
            break

    if len(band.users) == 0:
        band.delete()

    band.save()

def get_top_bands(max=None, sort=False, normalize=False, maxSize=6):
    bands = get_all_bands()
    top_bands = []
    top_band_size = 0;

    for band in bands:
        top_bands.append({"label": band.name, "size": len(band.users), "band_object": band})
        if len(band.users) > top_band_size:
            top_band_size = len(band.users)

    result = sorted(top_bands, key=itemgetter('size'), reverse=True)
    result = result[0:max]

    if normalize and top_band_size != 0:
        for band in result:
            band["size"] = int((maxSize * band["size"]) / top_band_size)

    if not sort:
        random.shuffle(result)

    return (result, len(bands))

def random_top_bands(max=None, user=None): #  Sorteia bandas baseado na quantidade de votos dela
    bands = get_all_bands(limit=100)
    removidos = {}
    bandas = []
    for band in bands:
        if not user or not user in band.users:
            for u in band.users:
                bandas.append(band)
                removidos[band.slug] = False

    bandasOrdenadas = []
    while len(bandas) > 0:
        tamanho = len(bandas)
        indice = random.randint(0, tamanho - 1)
        if not removidos[bandas[indice].slug]:
            bandasOrdenadas.append(bandas[indice])
            removidos[bandas[indice].slug] = True
        del bandas[indice]

    return bandasOrdenadas[0:max]

def get_random_bands_from_a_slug_list(slug_list, max=3):
    index = 0
    bands_slugs = []
    while index < max:
        slug = random.choice(slug_list)
        if not slug in bands_slugs:
            bands_slugs.append(slug)
            index += 1
    return [get_band(slug) for slug in bands_slugs]


def get_user_bands(user):
    bands = get_all_bands()
    return [band for band in bands if user in band.users]

def get_random_users(max=8):
    users = [user for user in User.objects.all()]
    users_random = set()
    len_users = 0
    if users:
        len_users = len(users)
        if max >= len_users:
            for user_index in range(len(users)):
                users[user_index].name = users[user_index].name.split(" ")[0]
            return (users, len_users)

        for i in range(max): # repete max vezes
            choice = random.choice(range(len(users)))
            user_random = users[choice]
            user_random.name = user_random.name.split(" ")[0]
            users_random.add(user_random)
            del users[choice]

    return (list(users_random), len_users)

def get_or_create_product(data):
    name = data['name'].title()
    slug = get_slug(data['slug']) if "slug" in data else get_slug(data['name'])
    try:
        product = Product.objects.get(slug=slug)
    except DoesNotExist:
        product = Product.objects.create(slug=slug, name=name)

    for prop in ["price", "photo", "quantity_type", "quantity_value"]:
        if prop in data and data[prop]:
            setattr(product, prop, data[prop])

    product.save()
    return product


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

def get_answers_and_counters_from_question(slugs):
    answers = []

    for slug in slugs:
        answers.extend(get_all_answers_from_question(slug))

    parcial = {}
    for answer in answers:
        if answer.answer in parcial.keys():
            parcial[answer.answer] += 1
        else:
            parcial[answer.answer] = 1

    resultado = parcial.items()
    return sorted(resultado, key=lambda tup: tup[1], reverse=True)


def validate_answers(data):
    if "musico-ou-fa" in data.keys() and (data["musico-ou-fa"] == "musico" or data["musico-ou-fa"] == "fa"):
        return True

    return False


def set_user_tipo(user, tipo):
    user.tipo = tipo
    user.save()
