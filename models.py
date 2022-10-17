from sqlalchemy import *
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Users(Base):
	__tablename__ = "users"
	
	id = Column(Integer, Identity(start = 1, cycle = False), primary_key = True, nullable = False)
	email = Column(String(75), nullable = False)
	username = Column(String(30), nullable = False, unique=True)
	role = Column(String(14), nullable = False)
	
class Calculators(Base):
	__tablename__ = "calculators"
	
	id = Column(Integer, Identity(start = 1, cycle = False), primary_key = True, nullable = False)
	name = Column(String(40), nullable = False)
	description = Column(String(256), nullable = True)
	input_data = Column(String(256), nullable = False) 
	code = Column(String(256), nullable = False, unique=True)
	codePrivacy = Column(Boolean, nullable = False)
	owner_id = Column(Integer, ForeignKey('users.id'), nullable = False)

class Reviews(Base):
	__tablename__ = "reviews"
	
	id = Column(Integer, Identity(start = 1, cycle = False), primary_key = True, nullable = False)
	message = Column(String(256), nullable = True)
	rating = Column(Integer, nullable = False)
	author_id = Column(Integer, ForeignKey('users.id'), nullable = False)
	calculator_id = Column(Integer, ForeignKey('calculators.id'), nullable = False)
	
	

 
