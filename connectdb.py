from re import U
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker, Session
from models import *
import pg8000


engine = create_engine("postgresql://admin:admin@localhost/pp", echo=False)

metadata = MetaData(engine)
Session = sessionmaker(bind=engine)
session = Session()
user1 = Users(username="Lkip", email="SkipOleg228@gmail.com", role="User" )
user2 = Users(username="Bzav3r", email="RusynVasylbruh@gmail.com", role="User")
session.add(user1)
session.add(user2)
session.commit()
calculator1 = Calculators(name="Area of rectangle", description="Calculates the area of a rectangle.", input_data="matrix -size=(1,4) -type=integer", code="https://pastebin.com/jNH8BiAb", codePrivacy=True, owner_id=user1.id)
calculator2 = Calculators(name="Area of rectangle", description="Calculates the area of a rectangle.", input_data="matrix -size=(1,4) -type=integer", code="https://pastebin.com/jNHBiAb", codePrivacy=True, owner_id=user1.id)
calculator3 = Calculators(name="Area of rectangle", description="Calculates the area of a rectangle.", input_data="matrix -size=(1,4) -type=integer", code="https://pastebin.com/jNH8BiA", codePrivacy=True, owner_id=user2.id)
session.add(calculator1)
session.add(calculator2)
session.add(calculator3)
session.commit()
review1 = Reviews(message="Very nice calculator!", rating=5, author_id=user1.id, calculator_id=calculator1.id)
review2 = Reviews(message="Very nice calculator!", rating=5, author_id=user1.id, calculator_id=calculator3.id)
session.add(review1)
session.add(review2)
session.commit()

res = session.query(Users).all()
print(res)
res = session.query(Calculators).all()
print(res)
res = session.query(Reviews).all()
print(res)

