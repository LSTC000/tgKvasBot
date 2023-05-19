from database import Alerts, BuyerInfo


async def delete_buyer_info(buyer_id: int) -> None:
    """
    :param buyer_id: Телеграм user id.
    """

    await Alerts.delete.where(Alerts.user_id == buyer_id).gino.scalar()
    await BuyerInfo.delete.where(BuyerInfo.buyer_id == buyer_id).gino.scalar()
