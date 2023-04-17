import datetime

from database.database_setup import BaseModel

from sqlalchemy import Column, BigInteger, SmallInteger, DateTime, sql, func


class SellerInfo(BaseModel):
    __tablename__ = 'seller_info'

    # Auto increment id.
    id = Column(BigInteger, primary_key=True, autoincrement=True,
                server_default=sql.text('nextval(\'seller_info_id_seq\')'))
    # Telegram user id.
    seller_id = Column(BigInteger, nullable=False)
    # Availability: 0 or 1.
    availability = Column(SmallInteger, nullable=False)
    # Working: 0 or 1.
    working = Column(SmallInteger, nullable=False)
    # Pause: 0 or 1.
    pause = Column(SmallInteger, nullable=False)
    # Update date.
    updated_date = Column(
        DateTime(True),
        default=datetime.datetime.utcnow,
        onupdate=datetime.datetime.utcnow,
        server_default=func.now()
    )

    query: sql.select
