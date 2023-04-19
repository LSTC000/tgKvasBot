from database.database_setup import BaseModel

from sqlalchemy import Column, VARCHAR, BigInteger, sql


class Brands(BaseModel):
    __tablename__ = 'brands'

    # Auto increment id.
    id = Column(BigInteger, primary_key=True, autoincrement=True,
                server_default=sql.text('nextval(\'brands_id_seq\')'))
    # Brand name.
    brand = Column(VARCHAR(32), nullable=False)

    query: sql.select
