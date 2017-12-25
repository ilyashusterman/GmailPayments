from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date, Float

Base = declarative_base()


class Payment(Base):
    __tablename__ = 'payment'

    id = Column(Integer, primary_key=True)
    title = Column(String)
    price = Column(Float)
    date = Column(Date)


class User(Base):
    __tablename = 'user'

    id = Column(Integer, primary_key=True)
    email = Column(String)


class Platform(Base):
    __tablename = 'platform'

    id = Column(Integer, primary_key=True)
    name = Column(String)
