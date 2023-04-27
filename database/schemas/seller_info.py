import datetime

from database.database_setup import BaseModel

from sqlalchemy import Column, BigInteger, VARCHAR, Float, SmallInteger, DateTime, sql, func


class SellerInfo(BaseModel):
    __tablename__ = 'seller_info'

    # Auto increment id.
    id = Column(BigInteger, primary_key=True, autoincrement=True,
                server_default=sql.text('nextval(\'seller_info_id_seq\')'))
    # Telegram user id.
    seller_id = Column(BigInteger, nullable=False)
    # City name.
    city = Column(VARCHAR(32), nullable=False)
    # Brand name.
    brand = Column(VARCHAR(32), nullable=False)
    # Availability: 0 or 1.
    availability = Column(SmallInteger, nullable=False)
    # Working: 0 or 1.
    working = Column(SmallInteger, nullable=False)
    # Pause: 0 or 1.
    pause = Column(SmallInteger, nullable=False)
    # Latitude coordinate.
    latitude = Column(Float, nullable=True)
    # Longitude coordinate.
    longitude = Column(Float, nullable=True)
    # Created date.
    created_date = Column(DateTime(True), server_default=func.now())
    # Update date.
    updated_date = Column(
        DateTime(True),
        default=datetime.datetime.utcnow,
        onupdate=datetime.datetime.utcnow,
        server_default=func.now()
    )

    query: sql.select
