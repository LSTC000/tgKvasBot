import string
import secrets


def create_secret_key() -> str:
    '''
    :return: Секретный ключ.
    '''

    alphabet = string.ascii_letters + string.digits

    return ''.join(secrets.choice(alphabet) for _ in range(32))
