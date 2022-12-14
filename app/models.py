from sqlalchemy import *
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class User(Base):
	__tablename__ = "users"

	id = Column(Integer, Identity(start = 1, cycle = False), primary_key = True, nullable = False)
	email = Column(String(75), nullable = False)
	username = Column(String(30), nullable = False, unique=True)
	role = Column(Integer, nullable = False)
	password = Column(String(100), nullable = False)
	
	review_child = relationship("Review", cascade="all,delete", backref="review_parent_user")
	calculator_child = relationship("Calculator", cascade="all,delete", backref="calculator_parent_user")

class Calculator(Base):
	__tablename__ = "calculators"

	id = Column(Integer, Identity(start = 1, cycle = False), primary_key = True, nullable = False)
	name = Column(String(40), nullable = False)
	description = Column(String(256), nullable = True)
	input_data = Column(String(256), nullable = False) 
	code = Column(String(256), nullable = False)
	is_public = Column(Boolean, nullable = False)
	author_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable = False)

	review_child = relationship("Review", cascade="all,delete", backref="review_parent_calculator")

class Review(Base):
	__tablename__ = "reviews"

	id = Column(Integer, Identity(start = 1, cycle = False), primary_key = True, nullable = False)
	message = Column(String(256), nullable = True)
	rating = Column(Integer, nullable = False)
	author_id = Column(Integer, ForeignKey('users.id'), nullable = False)
	calculator_id = Column(Integer, ForeignKey('calculators.id'), nullable = False)

