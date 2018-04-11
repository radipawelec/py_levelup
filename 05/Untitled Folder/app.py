from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


Base = automap_base()

engine = create_engine('sqlite:///sakila.db')
Session = sessionmaker(bind=engine)
session = Session()

all_actors = session.query(Actor)
print(all_actors)