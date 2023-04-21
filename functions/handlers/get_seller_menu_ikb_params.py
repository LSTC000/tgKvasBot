from data.callbacks import (
    AVAILABILITY_DATA,
    UNAVAILABILITY_DATA,
    START_WORKING_DATA,
    STOP_WORKING_DATA,
    START_PAUSE_DATA,
    STOP_PAUSE_DATA
)

from data.messages import (
    AVAILABILITY_IKB_MESSAGE,
    UNAVAILABILITY_IKB_MESSAGE,
    START_WORKING_IKB_MESSAGE,
    STOP_WORKING_IKB_MESSAGE,
    START_PAUSE_IKB_MESSAGE,
    STOP_PAUSE_IKB_MESSAGE
)

from database import get_seller_info


async def get_seller_menu_ikb_params(seller_id: int) -> dict:
    '''
    :param seller_id: Телеграм user id.
    :return: Словарь с параметрами для клавиатуры меню продавца.
    '''

    seller_info = await get_seller_info(seller_id)

    return {
        'availability_message': UNAVAILABILITY_IKB_MESSAGE if seller_info['availability'] else AVAILABILITY_IKB_MESSAGE,
        'working_message': STOP_WORKING_IKB_MESSAGE if seller_info['working'] else START_WORKING_IKB_MESSAGE,
        'pause_message': STOP_PAUSE_IKB_MESSAGE if seller_info['pause'] else START_PAUSE_IKB_MESSAGE,
        'availability_data': UNAVAILABILITY_DATA if seller_info['availability'] else AVAILABILITY_DATA,
        'working_data': STOP_WORKING_DATA if seller_info['working'] else START_WORKING_DATA,
        'pause_data': STOP_PAUSE_DATA if seller_info['pause'] else START_PAUSE_DATA
    }
