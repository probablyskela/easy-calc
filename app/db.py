from re import U
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker, Session
from app.models import *

engine = create_engine('postgresql+pg8000://postgres:123@localhost:5432/postgres', echo=False)

metadata = MetaData(engine)
Session = sessionmaker(bind=engine)
session = Session()

