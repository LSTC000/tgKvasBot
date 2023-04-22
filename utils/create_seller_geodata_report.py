def create_seller_geodata_report(seller_geodata_dict: dict) -> str:
    '''
    :param seller_geodata_dict: Словарь с геоданными продавца.
    :return: Сообщение с геоданными продавца.
    '''

    return f'<b>Геоданные:<b>\n\n' \
           f'<b>Город:<b> {seller_geodata_dict["city"]}' \
           f'<b>Бренд:<b> {seller_geodata_dict["brand"]}' \
           f'<b>Широта:<b> {seller_geodata_dict["latitude"]}' \
           f'<b>Долгота:<b> {seller_geodata_dict["longitude"]}' \
           f'<b>Адрес:<b> {seller_geodata_dict["address"]}' \
           f'<b>Ссылка на адрес:<b> {seller_geodata_dict["address_url"]}'
