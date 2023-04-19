import datetime

from database.database_setup import BaseModel

from sqlalchemy import Column, BigInteger, DateTime, sql, func


class Seller(BaseModel):
    __tablename__ = 'seller'

    # Auto increment id.
    id = Column(BigInteger, primary_key=True, autoincrement=True,
                server_default=sql.text('nextval(\'seller_id_seq\')'))
    # Telegram user id.
    seller_id = Column(BigInteger, nullable=False)
    # Created date.
    created_date = Column(DateTime(True), server_default=func.now())
    # Payment date.
    updated_date = Column(
        DateTime(True),
        default=datetime.datetime.utcnow,
        onupdate=datetime.datetime.utcnow,
        server_default=func.now()
    )

    # Были проблемы с налаживанием связи через foreign key с таблицами seller address и seller info
    # по атрибуту seller_id таблицы seller. Желательно это сделать и добавить каскадное удаление.

    query: sql.select
