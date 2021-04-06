from poll_fighters import models
from sqlalchemy import select, func, create_engine
from sqlalchemy.orm import sessionmaker
import pytest

# To Do:
# Make more tests
# Finish select_user and remove_user

def test_user_initilized_empty(session, engine):
    statement = select(func.count()).select_from(models.User)
    response = session.execute(statement)
    #assert response.scalar() == 0
    response.scalar().should.be.equal(0)

def test_add_user(session, engine):
    statement = select(func.count()).select_from(models.User)
    test_user = models.User('testuser', 'test@email.com')
    session.add(test_user)
    session.commit()
    session.execute(statement).scalar().should.be.equal(1)

def test_select_user(session, engine):
    statement = select(models.User).where(models.User.username == 'testuser')
    new_user = models.User('testuser', 'test@email.com')
    session.add(new_user)
    session.commit()
    #placeholder below for tests from yesterday
    session.execute(statement).scalars().one().username

def test_remove_user(session, engine):
    statement = select(func.count()).select_from(models.User)
    

@pytest.fixture
def session(engine):
    models.Base.metadata.create_all(engine)
    Session = sessionmaker(engine)
    session = Session()
    yield session
    models.Base.metadata.drop_all(engine)

@pytest.fixture
def engine():
    yield create_engine('sqlite:////tmp/apptests.db')
