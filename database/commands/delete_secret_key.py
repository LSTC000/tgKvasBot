from database import SecretKeys


async def delete_secret_key(user_id: int) -> None:
    """
    :param user_id: Телеграм user id.
    """

    return await SecretKeys.delete.where(SecretKeys.user_id == user_id).gino.scalar()
