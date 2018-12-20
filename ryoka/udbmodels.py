from sqlalchemy import Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Disease(Base):
    __tablename__ = 'diseases'

    id = Column(Integer, primary_key = True)
    name = Column(String(256))
