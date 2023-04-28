from database.database_setup import BaseModel

from sqlalchemy import Column, VARCHAR, BigInteger, sql


class SecretKeys(BaseModel):
    __tablename__ = 'secret_keys'

    # Auto increment id.
    id = Column(BigInteger, primary_key=True, autoincrement=True,
                server_default=sql.text('nextval(\'secret_keys_id_seq\')'))
    # Telegram user id.
    user_id = Column(BigInteger, nullable=True)
    # Secret key.
    secret_key = Column(VARCHAR(32), nullable=False)

    query: sql.select
