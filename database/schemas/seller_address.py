import datetime

from loader import tz

from database.database_setup import BaseModel

from sqlalchemy import Column, ForeignKey, BigInteger, VARCHAR, TEXT, DateTime, sql, func


class SellerAddress(BaseModel):
    __tablename__ = 'seller_coordinates'

    # Auto increment id.
    id = Column(BigInteger, primary_key=True, autoincrement=True,
                server_default=sql.text('nextval(\'seller_coordinate_id_seq\')'))
    # Telegram user id.
    seller_id = Column(BigInteger, ForeignKey('seller.seller_id'), nullable=False)
    # City name.
    city = Column(VARCHAR(32), nullable=False)
    # Brand name.
    brand = Column(VARCHAR(32), nullable=False)
    # Latitude coordinate.
    latitude = Column(VARCHAR(32), nullable=True)
    # Longitude coordinate.
    longitude = Column(VARCHAR(32), nullable=True)
    # Seller address.
    address = Column(TEXT, nullable=True)
    # Url for seller address.
    address_url = Column(TEXT, nullable=True)
    # Update date.
    updated_date = Column(
        DateTime(True),
        default=datetime.datetime.utcnow,
        onupdate=datetime.datetime.utcnow,
        server_default=func.now(tz)
    )

    query: sql.select
