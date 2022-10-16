from sqlalchemy import Column, Integer, String, Float
from database import Base 

class Address(Base):
    __tablename__ = 'address.book'
    id = Column(Integer, primary_key=True)
    first_name = Column(String(256))
    last_name = Column(String(256))
    age = Column(Integer())
    mobile_no = Column(Integer())
    city = Column(String(25))
    state = Column(String(25))
    country = Column(String(25))
    latitude = Column(Float())
    longitude = Column(Float())

