from data.config import MAPS_GEOCODER_TOKEN, MAPS_GEOCODER_URL, MAPS_SEARCH_URL

import requests

url = MAPS_GEOCODER_URL.format(MAPS_GEOCODER_TOKEN, '53.347570', '83.776102')
response = requests.get(url=url).json()
text = response['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['metaDataProperty']['GeocoderMetaData']['text']

print(text, MAPS_SEARCH_URL.format('83.776102', '53.347570'))
