from loader import tz

from database.database_setup import BaseModel

from sqlalchemy.orm import relationship
from sqlalchemy import Column, BigInteger, DateTime, sql, func


class Seller(BaseModel):
    __tablename__ = 'seller'

    # Auto increment id.
    id = Column(BigInteger, primary_key=True, autoincrement=True,
                server_default=sql.text('nextval(\'seller_id_seq\')'))
    # Telegram user id.
    seller_id = Column(BigInteger, nullable=False)
    # Created date.
    created_date = Column(DateTime(True), server_default=func.now(tz))
    # Добавим связь один-ко-многим между таблицами seller и seller_info, seller и seller_coordinates.
    # cascade='all, delete' указывает, что при удалении записи из таблицы seller
    # должны быть удалены связанные записи в таблице seller_info и seller_coordinates.
    seller_info = relationship("SellerInfo", cascade='all, delete', backref="seller")
    seller_coordinates = relationship("SellerCoordinates", cascade='all, delete', backref="seller")

    query: sql.select
