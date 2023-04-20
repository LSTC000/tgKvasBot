from typing import Union

from database import Buyer


async def update_buyer_brand(buyer_id: int, brand: Union[str, None]):
    """
    :param buyer_id: Телеграм user id.
    :param brand: Новый выбранный бренд пользователя.
    """

    await Buyer.update.values(brand=brand).where(Buyer.buyer_id == buyer_id).gino.scalar()
