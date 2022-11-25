from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker, Session
from app.models import *
from app import app
engine = create_engine(app.config['DATABASE'], echo=False)

metadata = Base.metadata

Session = sessionmaker(bind=engine)
session = Session()
