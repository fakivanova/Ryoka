from sqlalchemy import Column, String, Integer, ForeignKey, Table
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

employees_diseases = Table('employees_diseases', Base.metadata,
                           Column('employee_id', ForeignKey('employees.id'), primary_key=True),
                           Column('disease_id', ForeignKey('diseases.id'), primary_key=True))

employees_equipments = Table('employees_equipments', Base.metadata,
                             Column('employee_id', ForeignKey('employees.id'), primary_key=True),
                             Column('equipment_id', ForeignKey('equipments.id'), primary_key=True))

class Disease(Base):
    __tablename__ = 'diseases'

    id = Column(Integer, primary_key = True)
    name = Column(String(256))
    employees = relationship('Employee', secondary=employees_diseases, back_populates='diseases')

class Equipment(Base):
    __tablename__ = 'equipments'

    id = Column(Integer, primary_key = True)
    name = Column(String(256))
    employees = relationship('Employee', secondary=employees_equipments, back_populates='equipments')

class Degree(Base):
    __tablename__ = 'degrees'

    id = Column(Integer, primary_key = True)
    name = Column(String(256))
    employees = relationship('Employee', back_populates='degree', lazy='dynamic')


class Employee(Base):
    __tablename__ = 'employees'

    id = Column(Integer, primary_key = True)
    name = Column(String(256))
    experience = Column(Integer)
    degree_id = Column(Integer, ForeignKey('degrees.id'))
    degree = relationship('Degree', back_populates='employees')
    diseases = relationship('Disease', secondary=employees_diseases, back_populates='employees')
    equipments = relationship('Equipment', secondary=employees_equipments, back_populates='employees')


