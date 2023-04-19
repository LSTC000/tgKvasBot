from database.database_setup import BaseModel

from sqlalchemy import Column, VARCHAR, BigInteger, sql


class Cities(BaseModel):
    __tablename__ = 'cities'

    # Auto increment id.
    id = Column(BigInteger, primary_key=True, autoincrement=True,
                server_default=sql.text('nextval(\'cities_id_seq\')'))
    # City name.
    city = Column(VARCHAR(32), nullable=False)

    query: sql.select
