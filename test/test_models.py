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

def test_question_hayden(session):
    # Creating 2 question types
    for t in ['Open', 'Multiple Choice']:
        new_type = models.QuestionType(t)
        session.add(new_type)
    session.commit()

    # Create a question

    new_question = models.Question(text='pizza',question_type_id=new_type.id)

def test_add_multiple_question_to_poll(session):
    # Creates a single type for questions
    multiple_type = models.QuestionType('Multiple Choice')
    session.add(multiple_type)
    session.commit()

    # Creates multiple questions using a single type
    first_question = models.Question(text='pizza', question_type_id=multiple_type.id)
    second_question = models.Question(text='sushi', question_type_id=multiple_type.id)
    third_question = models.Question(text='tacos', question_type_id=multiple_type.id)
    session.add(first_question)
    session.add(second_question)
    session.add(third_question)
    session.commit()
    
    # Creates a poll using the three questions made above
    food_poll = models.Poll(description="What are your favorite foods?", questions=[first_question,second_question,third_question])
    session.add(food_poll)
    session.commit()

    # Selects the poll from the database and asserts that it was assigned all three questions from above
    select_statement = select(models.Poll).where(models.Poll.id == food_poll.id)
    response = session.execute(select_statement)
    queried_poll = response.first()[0]
    assert queried_poll.questions == [first_question, second_question, third_question]

def test_add_multiple_qestions_of_different_types_in_poll(session):
    # Creates multiple types for questions
    multiple_type = models.QuestionType('Multiple Choice')
    open_type = models.QuestionType('Open Ended')
    session.add(multiple_type)
    session.add(open_type)
    session.commit()

    # Creates Multiple question using the different types above
    multiple_question = models.Question(text='Minecraft', question_type_id=multiple_type.id)
    open_question = models.Question(text='What is the meaning of life', question_type_id=open_type.id)
    session.add(multiple_question)
    session.add(open_question)
    session.commit()

    # Creates a poll that includes the different question above
    random_poll = models.Poll(description='Random questions about life', questions=[multiple_question, open_question])
    session.add(random_poll)
    session.commit()

    #
    select_statement = select(models.Poll).where(models.Poll.id == random_poll.id)
    response = session.execute(select_statement)
    queried_poll = response.first()[0]
    queried_poll.questions.should.contain(open_question)
    queried_poll.questions.should.contain(multiple_question)

def test_add_multiple_polls(sessions):
    pass

def find_all_multiple_choice_questions_in_poll(session):
    multiple_type = models.QuestionType('Multiple Choice')
    open_type = models.QuestionType('Open Ended')
    session.add(multiple_type)
    session.add(open_type)
    session.commit()

    multiple_question_first = models.Question(text='Minecraft', question_type_id=multiple_type.id)
    multiple_question_second = models.Question(text='Roblox', question_type_id=multiple_type.id)
    multiple_question_third = models.Question(text='Apex Legends', question_type_id=multiple_type.id)
    session.add(multiple_question_first)
    session.add(multiple_question_second)
    session.add(multiple_question_third)
    
    open_question_first = models.Question(text='What is the meaning of life', question_type_id=open_type.id)
    open_question_second = models.Question(text='what is love', question_type_id=open_type.id)
    session.add(open_question_first)
    session.add(open_question_second)
    
    session.commit()

    questions_list=[multiple_question_first, multiple_question_second, multiple_question_third, open_question_first, open_question_second]
    random_poll = models.Poll(description='Super Random questions about life', questions=questions_list)
    session.add(random_poll)
    session.commit()

    select_statement = select(models.Poll).where(models.Poll.question_type_id == multiple_type.id)
    response = session.execute(select_statement)
    queried_poll = response.first()[0]
    # To Do: 
    # Having trouble quering for questions by type and poll id
    # Implement using join

def test_choice_initialized_empty(session):
    pass 

def test_add_choice(session):
    pass 

def test_select_choice(session):
    pass 

def test_remove_choice(session):
    pass 

def test_question_ids_of_poll(session):
    pass

# Make it possible to passthrough name as argument    
def create_users(amount):
    for i in range(amount):
        yield models.User(f'testuser{i}', f'test{i}@email.com')

def questions():
    while True:
        text, question_type = yield
        yield models.Question(text, question_type)

@pytest.fixture
def session(engine):
    models.Base.metadata.create_all(engine)
    Session = sessionmaker(engine)
    session = Session()
    yield session
    session.commit()
    models.Base.metadata.drop_all(engine)

@pytest.fixture
def engine():
    yield create_engine('postgresql://testuser:testpassword@localhost:55432/testdb')
