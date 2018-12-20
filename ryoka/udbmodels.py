from sqlalchemy import Column, String, Integer, Table
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Disease(Base):
    __tablename__ = 'diseases'

    id = Column(Integer, primary_key = True)
    name = Column(String(256))
    
class Equipment(Base):
    __tablename__ = 'equipments'

    id = Column(Integer, primary_key = True)
    name = Column(String(256))

class Degree(Base):
    __tablename__ = 'degrees'

    id = Column(Integer, primary_key = True)
    name = Column(String(256))
    employees = relationship('Employee', back_populate='degree', lazy='dynamic')

class Employee(Base):
    __tablename__ = 'employees'

    id = Column(Integer, primary_key = True)
    name = Column(String(256))
    experience = Column(Integer)
    degree_id = Column(Integer, ForeignKey('degrees.id'))
    degree = relationship('Degree', back_populate='employees')

