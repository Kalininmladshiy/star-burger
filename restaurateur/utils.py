import requests
from environs import Env

env = Env()
env.read_env()


def fetch_coordinates(address):
    base_url = "https://geocode-maps.yandex.ru/1.x"
    apikey = env('API_KEY_YANDEX')
    response = requests.get(base_url, params={
        "geocode": address,
        "apikey": apikey,
        "format": "json",
    })
    response.raise_for_status()
    found_places = response.json()['response']['GeoObjectCollection']['featureMember']

    if not found_places:
        return None

    most_relevant = found_places[0]
    lon, lat = most_relevant['GeoObject']['Point']['pos'].split(" ")
    return lat, lon
