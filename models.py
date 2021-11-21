from sqlalchemy import (
    MetaData, Table, Column,
    Integer, String, Date, Float,
)

meta = MetaData()

price = Table(
    'historical_data', meta,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('currency', String(45), nullable=False),
    Column('date', Date, nullable=False),
    Column('price', Float(20), nullable=False)
)