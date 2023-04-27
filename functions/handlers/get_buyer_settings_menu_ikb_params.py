from data.callbacks import ON_ALERT_DATA, OFF_ALERT_DATA

from data.messages import ON_ALERT_IKB_MESSAGE, OFF_ALERT_IKB_MESSAGE

from database import get_alert


async def get_buyer_settings_menu_ikb_params(buyer_id: int) -> dict:
    '''
    :param buyer_id: Телеграм user id.
    :return: Словарь с параметрами для клавиатуры меню настроек покупателя.
    '''

    alert = await get_alert(buyer_id)

    return {
        'alert_message': OFF_ALERT_IKB_MESSAGE if alert else ON_ALERT_IKB_MESSAGE,
        'alert_data': OFF_ALERT_DATA if alert else ON_ALERT_DATA
    }
