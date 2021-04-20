from poll_fighters import models
from sqlalchemy import select, func, create_engine, delete
from sqlalchemy.orm import sessionmaker
import pytest, random

# To Do:
# Make more tests
# Finish remove_user

def test_user_initilized_empty(session):
    statement = select(func.count()).select_from(models.User)
    response = session.execute(statement)
    response.scalar().should.be.equal(0)

def test_add_user(session):
    for new_user in create_users(1):
        session.add(new_user)
        session.commit()
        statement = select(func.count()).select_from(models.User)
        session.execute(statement).scalar().should.be.equal(1)

def test_select_user(session):
    for new_user in create_users(1):
        session.add(new_user)
        session.commit()
        statement = select(models.User).where(models.User.username == new_user.username)
        session.execute(statement).scalars().one().should.be.equal(new_user)

def test_remove_user(session):
    # Validates that the table starts empty
    count_statement = select(func.count()).select_from(models.User)
    count_response = session.execute(count_statement)
    count_response.scalar().should.be.equal(0)
    
    # Add 3 users to the table
    new_users = list(create_users(3))
    for new_user in new_users:
        session.add(new_user)
        session.commit()
        select_statement = select(models.User).where(models.User.id == new_user.id)
        # Asserts that the user has been inserted into the table
        session.execute(select_statement).scalars().one().should.be.equal(new_user)

    # Randomly chooses a user to delete
    rdm_user = random.choice(new_users)
    assert session.get(models.User, rdm_user.id) != None
    session.delete(rdm_user)
    session.flush()
    # assert session.get(models.User, rdm_user.id) == None

def test_change_user_name(session):
    for new_user in create_users(2):
        session.add(new_user)
        session.commit()
    
def test_change_user_email(session):
    for new_user in create_users(2):
        session.add(new_user)
        session.commit()

def test_change_user_passwd(session):
    for new_user in create_users(1):
        session.add(new_user)
        session.commit()

def test_poll_initilized_empty(session):
    return

def test_add_poll(session):
    return

def test_select_poll(session):
    return 

def test_remove_poll(session):
    return 

def test_question_initialized_empty(session):
    return 

def test_add_question(session):
    return 

def test_select_question(session):
    return 

def test_remove_question(session):
    return 

def test_choice_initialized_empty(session):
    return 

def test_add_choice(session):
    return 

def test_select_choice(session):
    return 

def test_remove_choice(session):
    return 

def test_question_ids_of_poll(session):
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
    print('going to drop tables')
    models.Base.metadata.drop_all(engine)
    print('tables successfully dropped')

@pytest.fixture
def engine():
    yield create_engine('sqlite:////tmp/apptests.db')
