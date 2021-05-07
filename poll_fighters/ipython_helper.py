from poll_fighters import models
from sqlalchemy import select, func, create_engine, delete
from sqlalchemy.orm import sessionmaker

def get_engine():
    return create_engine('postgresql://user:password@localhost:5555/playgrounddb')

def get_session(engine=get_engine()):
    models.Base.metadata.create_all(engine)
    Session = sessionmaker(engine)
    session = Session()
    return session
