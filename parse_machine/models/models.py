from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date, Float

Base = declarative_base()


class Payment(Base):
    __tablename__ = 'payment'

    id = Column(Integer, primary_key=True)
    title = Column(String)
    price = Column(Float)
    date = Column(Date)

