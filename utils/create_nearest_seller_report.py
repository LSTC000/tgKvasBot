def create_nearest_seller_report(nearest_seller_dict: dict) -> str:
    '''
    :param nearest_seller_dict: Словарь с данныит продавца для покупателя.
    :return: Сообщение с данными о продавце для покупателя.
    '''

    return f'<b>Работает</b>: {"Да" if nearest_seller_dict["working"] else "Нет"}\n\n' \
           f'<b>Наличе</b>: {"Есть" if nearest_seller_dict["availability"] else "Нет"}\n\n' \
           f'<b>Продавец ушёл на перерыв</b>: {"Да" if nearest_seller_dict["pause"] else "Нет"}\n\n' \
           f'<b>Геолокация продавца</b> 👇'
