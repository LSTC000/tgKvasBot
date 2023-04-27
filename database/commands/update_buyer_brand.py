from typing import Union

from database import BuyerInfo


async def update_buyer_brand(buyer_id: int, brand: Union[str, None]) -> None:
    """
    :param buyer_id: Телеграм user id.
    :param brand: Новый выбранный бренд покупателя.
    """

    await BuyerInfo.update.values(brand=brand).where(BuyerInfo.buyer_id == buyer_id).gino.scalar()
