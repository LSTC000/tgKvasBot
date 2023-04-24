def create_nearest_seller_report(nearest_seller_dict: dict) -> str:
    '''
    :param nearest_seller_dict: Словарь с данныит продавца для покупателя.
    :return: Сообщение с данными о продавце для покупателя.
    '''

    return f'<b>Продавец ушёл на перерыв</b>: {"Да" if nearest_seller_dict["pause"] else "Нет"}\n\n' \
           f'<b>Адрес</b>: <a href="{nearest_seller_dict["address_url"]}" title="address">' \
           f'{nearest_seller_dict["address"]}</a>'
