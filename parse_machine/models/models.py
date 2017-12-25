from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date, Float, ForeignKey
from sqlalchemy.orm import relationship

Base = declarative_base()


class Payment(Base):
    __tablename__ = 'payment'

    id = Column(Integer, primary_key=True)
    platform_id = Column(Integer, ForeignKey("platform.id"))
    user_id = Column(Integer, ForeignKey("user.id"))
    title = Column(String)
    price = Column(Float)
    date = Column(Date)

    platform = relationship("Platform", foreign_keys=[platform_id])
    user = relationship("User", foreign_keys=[user_id])


class User(Base):
    __tablename = 'user'

    id = Column(Integer, primary_key=True)
    email = Column(String)


class Platform(Base):
    __tablename = 'platform'

    id = Column(Integer, primary_key=True)
    name = Column(String)
