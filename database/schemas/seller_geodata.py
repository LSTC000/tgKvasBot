import datetime

from database.database_setup import BaseModel

from sqlalchemy import Column, BigInteger, Float, VARCHAR, TEXT, DateTime, sql, func


class SellerGeodata(BaseModel):
    __tablename__ = 'seller_geodata'

    # Auto increment id.
    id = Column(BigInteger, primary_key=True, autoincrement=True,
                server_default=sql.text('nextval(\'seller_geodata_id_seq\')'))
    # Telegram user id.
    seller_id = Column(BigInteger,  nullable=False)
    # City name.
    city = Column(VARCHAR(32), nullable=False)
    # Brand name.
    brand = Column(VARCHAR(32), nullable=False)
    # Latitude coordinate.
    latitude = Column(Float, nullable=True)
    # Longitude coordinate.
    longitude = Column(Float, nullable=True)
    # Seller address.
    address = Column(TEXT, nullable=True)
    # Url for seller address.
    address_url = Column(TEXT, nullable=True)
    # Update date.
    updated_date = Column(
        DateTime(True),
        default=datetime.datetime.utcnow,
        onupdate=datetime.datetime.utcnow,
        server_default=func.now()
    )

    query: sql.select
