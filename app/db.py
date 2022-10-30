from re import U
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker, Session
from app.models import *
import pg8000

from alembic.config import Config

database_str = Config('sqlalchemy.url')
engine = create_engine("postgresql://admin:admin@localhost/pp", echo=False)

metadata = MetaData(engine)
Session = sessionmaker(bind=engine)
session = Session()

