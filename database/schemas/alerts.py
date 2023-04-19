from database.database_setup import BaseModel

from sqlalchemy import Column, BigInteger, sql


class Alerts(BaseModel):
    __tablename__ = 'alerts'

    # Auto increment id.
    id = Column(BigInteger, primary_key=True, autoincrement=True,
                server_default=sql.text('nextval(\'alerts_id_seq\')'))
    # Telegram user id.
    user_id = Column(BigInteger, nullable=False)

    query: sql.select
