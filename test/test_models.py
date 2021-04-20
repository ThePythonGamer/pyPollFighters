from poll_fighters import models
from sqlalchemy import select, func, create_engine
from sqlalchemy.orm import sessionmaker
import pytest

# To Do:
# Make more tests
# Finish remove_user

def test_user_initilized_empty(session, engine):
    statement = select(func.count()).select_from(models.User)
    response = session.execute(statement)
    #assert response.scalar() == 0
    response.scalar().should.be.equal(0)

def test_add_user(session, engine):
    for new_user in create_users(1):
        session.add(new_user)
        session.commit()
        statement = select(func.count()).select_from(models.User)
        session.execute(statement).scalar().should.be.equal(1)

def test_select_user(session, engine):
    for new_user in create_users(1):
        session.add(new_user)
        session.commit()
        statement = select(models.User).where(models.User.username == new_user.username)
        session.execute(statement).scalars().one().should.be.equal(new_user)

def test_remove_user(session, engine):
    for new_user in create_users(3):
        statement = select(func.count()).select_from(models.User)

def test_change_user_name(session, engine):
    for new_user in create_users(2):
        session.add(new_user)
        session.commit()
    
def test_change_user_email(session, engine):
    for new_user in create_users(2):
        session.add(new_user)
        session.commit()

def test_change_user_passwd(session, engine):
    for new_user in create_users(1):
        session.add(new_user)
        session.commit()

def test_poll_initilized_empty(session, engine):
    return

def test_add_poll(session, engine):
    return

def test_select_poll(session, engine):
    return 

def test_remove_poll(session, engine):
    return 

def test_question_initialized_empty(session, engine):
    return 

def test_add_question(session, engine):
    return 

def test_select_question(session, engine):
    return 

def test_remove_question(session, engine):
    return 

def test_choice_initialized_empty(session, engine):
    return 

def test_add_choice(session, engine):
    return 

def test_select_choice(session, engine):
    return 

def test_remove_choice(session, engine):
    return 

def test_question_ids_of_poll(session, engine):
    return

# Make it possible to passthrough name as argument    
def create_users(amount):
    for i in range(amount):
        yield models.User(f'testuser{i}', f'test{i}@email.com')

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
