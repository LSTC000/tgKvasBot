def create_nearest_seller_report(nearest_seller_dict: dict) -> str:
    '''
    :param nearest_seller_dict: Словарь с данныит продавца для покупателя.
    :return: Сообщение с данными о продавце для покупателя.
    '''

    return f'📌 <b>Работает</b>: {"да." if nearest_seller_dict["working"] else "нет."}\n\n' \
           f'📌 <b>Наличие кваса</b>: {"есть." if nearest_seller_dict["availability"] else "нет."}\n\n' \
           f'📌 <b>Перерыв</b>: {"да." if nearest_seller_dict["pause"] else "нет."}\n\n' \
           f'🌐 Геолокация продавца 👇'
