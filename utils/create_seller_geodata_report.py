def create_seller_geodata_report(seller_geodata_dict: dict) -> str:
    '''
    :param seller_geodata_dict: Словарь с геоданными продавца.
    :return: Сообщение с геоданными продавца.
    '''

    return f'🏠 <b>Город:</b> {seller_geodata_dict["city"]}.\n\n' \
           f'💼 <b>Бренд:</b> {seller_geodata_dict["brand"]}.\n\n' \
           f'📍 <b>Широта:</b> {seller_geodata_dict["latitude"]}.\n\n' \
           f'📍 <b>Долгота:</b> {seller_geodata_dict["longitude"]}.\n\n' \
           f'🔍 <b>Адрес:</b> <a href="{seller_geodata_dict["address_url"]}" title="address">' \
           f'{seller_geodata_dict["address"]}</a>.\n\n' \
