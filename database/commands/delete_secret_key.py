from typing import Union

from database import SecretKeys


async def delete_secret_key(user_id: Union[int, str]) -> None:
    """
    :param user_id: Телеграм user id или секретный ключ.
    """

    if isinstance(user_id, int):
        return await SecretKeys.delete.where(SecretKeys.user_id == user_id).gino.scalar()
    else:
        return await SecretKeys.delete.where(SecretKeys.secret_key == user_id).gino.scalar()
