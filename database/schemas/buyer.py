import datetime

from database.database_setup import BaseModel

from sqlalchemy import Column, VARCHAR, BigInteger, DateTime, sql, func


class Buyer(BaseModel):
    __tablename__ = 'buyer'

    # Auto increment id.
    id = Column(BigInteger, primary_key=True, autoincrement=True,
                server_default=sql.text('nextval(\'buyer_id_seq\')'))
    # Telegram user id.
    buyer_id = Column(BigInteger, nullable=False)
    # City name.
    city = Column(VARCHAR(32), nullable=False)
    # Brand name.
    brand = Column(VARCHAR(32), nullable=True)
    # Created date.
    created_date = Column(DateTime(True), server_default=func.now())
    # Payment date.
    updated_date = Column(
        DateTime(True),
        default=datetime.datetime.utcnow,
        onupdate=datetime.datetime.utcnow,
        server_default=func.now()
    )

    query: sql.select
