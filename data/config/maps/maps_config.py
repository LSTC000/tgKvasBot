import os

from dotenv import load_dotenv
from dotenv import find_dotenv

load_dotenv(find_dotenv())

MAPS_GEOCODER_TOKEN = os.getenv('MAPS_GEOCODER_TOKEN')

MAPS_GEOCODER_URL = 'https://geocode-maps.yandex.ru/1.x/?apikey={}&geocode={},{}&format=json&sco=latlong&results=1&lang=ru_RU'

MAPS_SEARCH_URL = 'https://maps.yandex.ru/?ll={},{}&z=22'
