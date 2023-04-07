from typing import Union
from json import JSONDecodeError

from data.config import HEADERS
from data.config import MAPS_GEOCODER_TOKEN, MAPS_GEOCODER_URL, MAPS_SEARCH_URL

import httpx


def create_address_url(chat_id: str, longitude: str, latitude: str) -> Union[None, str]:
    """
    :param chat_id: Телеграм chat id пользователя.
    :param longitude: Долгота.
    :param latitude: Широта.
    :return: Если не возникла ошибка, то возвращаем гиперссылку с адресом ближайшей бочки с квасом.
        Иначе возваращаем None.
    """

    # Формируем ссылку для запроса к сервису Яндекс.Карты с целью получить адрес ближайшей бочки с квасом по
    # координатам долготы и широты.
    url = MAPS_GEOCODER_URL.format(MAPS_GEOCODER_TOKEN, longitude, latitude)

    # Отправляем асинхронный запрос и обрабатываем возможные ошибки
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url=url, headers=HEADERS, params={'chat_id': chat_id})
    except (httpx.HTTPError, httpx.RequestError, httpx.TimeoutException):
        return None

    # Начинаем доставать адркс из json, обрабатывая все возможные ошибки
    try:
        # Достаём json из ответа на запрос
        data = response.json()
        # Из json достаём строку с адресом
        address = data['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['metaDataProperty']['GeocoderMetaData']['text']
    except (JSONDecodeError, KeyError, IndexError, AttributeError, TypeError, FileNotFoundError, IOError):
        return None

    # Формируем гиперссылку и отправляем её в качестве ответа функции
    return f'<a href="{MAPS_SEARCH_URL.format(longitude, latitude)}" title="адрес"><b>{address}</b></a>.'
