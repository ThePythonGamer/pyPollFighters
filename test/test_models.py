from poll_fighters import models
from sqlalchemy import select, func, create_engine, delete
from sqlalchemy.orm import sessionmaker
import pytest, random

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

def test_add_multiple_question_to_poll(session):
    #Creates a user for the the response user id
    for new_user in create_users(1):
        session.add(new_user)
        session.commit()

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
        food_poll = models.Poll(creator_id=new_user.id, description="What are your favorite foods?", questions=[first_question,second_question,third_question])
        session.add(food_poll)
        session.commit()

        # Selects the poll from the database and asserts that it was assigned all three questions from above
        select_statement = select(models.Poll).where(models.Poll.id == food_poll.id)
        response = session.execute(select_statement)
        queried_poll = response.first()[0]
        assert queried_poll.questions == [first_question, second_question, third_question]

def test_add_multiple_qestions_of_different_types_in_poll(session):
    #Creates a user for the the response user id
    for new_user in create_users(1):
        session.add(new_user)
        session.commit()

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
        random_poll = models.Poll(creator_id=new_user.id, description='Random questions about life', questions=[multiple_question, open_question])
        session.add(random_poll)
        session.commit()

        # Checks that the poll includes both an open and multiple choice question
        select_statement = select(models.Poll).where(models.Poll.id == random_poll.id)
        response = session.execute(select_statement)
        queried_poll = response.first()[0]
        queried_poll.questions.should.contain(open_question)
        queried_poll.questions.should.contain(multiple_question)

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
    statement = select(func.count()).select_from(models.Choice)
    response = session.execute(statement)
    response.scalar().should.be.equal(0)

def test_add_choice(session):
    # Create a multiple choice type for questions
    multiple_type = models.QuestionType('Multiple Choice')
    session.add(multiple_type)
    session.commit()

    # Create a question with the multiple choice type
    multiple_question = models.Question(text='What is the meaning of life', question_type_id=multiple_type.id)
    session.add(multiple_question)
    session.commit()

    # Create all the choices associated to the previous question
    choice1 = models.Choice(text='42', question_id=multiple_question.id)
    choice2 = models.Choice(text='happiness', question_id=multiple_question.id)
    choice3 = models.Choice(text='nothing', question_id=multiple_question.id)
    session.add(choice1)
    session.add(choice2)
    session.add(choice3)
    session.commit()

    # Checking that all choices have been added
    statement = select(func.count()).select_from(models.Choice)
    session.execute(statement).scalar().should.be.equal(3)

    # Checking that the choices added are the same as the ones created above
    select_statement = select(models.Choice)
    response = session.execute(select_statement)
    queried_choice = [choice for subtpl in response.all() for choice in subtpl]
    [choice1, choice2, choice3].should.equal(queried_choice)

def test_select_choice_by_question_id(session):
    # Create a multiple choice type for questions
    multiple_type = models.QuestionType('Multiple Choice')
    session.add(multiple_type)
    session.commit()

    # Create two different questions with the multiple choice type
    multiple_question1 = models.Question(text='What is the meaning of life', question_type_id=multiple_type.id)
    multiple_question2 = models.Question(text='What is your favorite colour', question_type_id=multiple_type.id)
    session.add(multiple_question1)
    session.add(multiple_question2)
    session.commit()

    # Create all the choices for the first question
    q1_choice1 = models.Choice(text='42', question_id=multiple_question1.id)
    q1_choice2 = models.Choice(text='happiness', question_id=multiple_question1.id)
    q1_choice3 = models.Choice(text='nothing', question_id=multiple_question1.id)
    session.add(q1_choice1)
    session.add(q1_choice2)
    session.add(q1_choice3)

    # Create all the choices for the second question
    q2_choice1 = models.Choice(text='red', question_id=multiple_question2.id)
    q2_choice2 = models.Choice(text='green', question_id=multiple_question2.id)
    q2_choice3 = models.Choice(text='blue', question_id=multiple_question2.id)
    session.add(q2_choice1)
    session.add(q2_choice2)
    session.add(q2_choice3)
    session.commit()

    # Checking that all choices have been added
    statement = select(func.count()).select_from(models.Choice)
    session.execute(statement).scalar().should.be.equal(6)

    # Checking that the only choices for question 2 are the ones associated to that one
    select_statement = select(models.Choice).where(models.Choice.question_id == multiple_question2.id)
    response = session.execute(select_statement)
    queried_choice = [choice for subtpl in response.all() for choice in subtpl]
    [q2_choice1, q2_choice2, q2_choice3].should.equal(queried_choice)

def test_remove_choice(session):
    # Create a multiple choice type for questions
    multiple_type = models.QuestionType('Multiple Choice')
    session.add(multiple_type)
    session.commit()

    # Create a question with the multiple choice type
    multiple_question = models.Question(text='What is the meaning of life', question_type_id=multiple_type.id)
    session.add(multiple_question)
    session.commit()

    # Create all the choices for the question
    choice1 = models.Choice(text='42', question_id=multiple_question.id)
    choice2 = models.Choice(text='happiness', question_id=multiple_question.id)
    choice3 = models.Choice(text='nothing', question_id=multiple_question.id)
    session.add(choice1)
    session.add(choice2)
    session.add(choice3)
    session.commit()

    # Verifies that the choices were added
    statement = select(func.count()).select_from(models.Choice)
    session.execute(statement).scalar().should.be.equal(3)

    # Removes a choice from the question
    choice_to_delete = choice3
    session.delete(choice_to_delete)
    session.flush()
    
    # Verifies that there are only 2 choices now
    statement = select(func.count()).select_from(models.Choice)
    session.execute(statement).scalar().should.be.equal(2)

    # Verifies that the correct choice was deleted
    statement = select(models.Choice).where(models.Choice.id == choice_to_delete.id)
    response = session.execute(statement)
    list(response).should.be.empty

def test_response_initialized_empty(session):
    statement = select(func.count()).select_from(models.ResponseOpen)
    response = session.execute(statement)
    response.scalar().should.be.equal(0)

def test_response_open_relationships(session):
    #Creates a user for the the response user id
    for new_user in create_users(1):
        session.add(new_user)
        session.commit()

        #Creates a type of question to be used
        open_type = models.QuestionType('Open Ended')
        session.add(open_type)
        session.commit()

        #Creates a question for the poll
        open_question = models.Question(text='What is the meaning of life', question_type_id=open_type.id)
        session.add(open_question)
        session.commit()

        #Creates a poll to be used in the response
        random_poll = models.Poll(creator_id=new_user.id, description='Super Random questions about life', questions=[open_question])
        session.add(random_poll)
        session.commit()

        #Create a response
        user_response_text = "the meaning of life is 42" 
        user_response = models.ResponseOpen(poll_id=random_poll.id, responder_user_id=new_user.id, question_id=open_question.id, open_response=user_response_text)
        session.add(user_response)
        session.commit()
        
        #Verify that there are relationships
        select_statement = select(models.ResponseOpen)
        response = session.execute(select_statement)
        queried_response = response.first()[0]
        assert queried_response.poll == random_poll
        assert queried_response.responder_user == new_user
        assert queried_response.question == open_question
        assert queried_response.open_response == user_response_text

def test_response_choice_initialized_empty(session):
    statement = select(func.count()).select_from(models.ResponseChoice)
    response = session.execute(statement)
    response.scalar().should.be.equal(0)

def test_response_choice_relationships(session):
    # Creates a user for the the response user id
    for new_user in create_users(1):
        session.add(new_user)
        session.commit()

        # Creates a type of question to be used
        multiple_type = models.QuestionType('Multiple Choice')
        session.add(multiple_type)
        session.commit()

        # Creates a question for the poll
        multiple_question = models.Question(text='What is the meaning of life', question_type_id=multiple_type.id)
        session.add(multiple_question)
        session.commit()
        
        # Creates the choices for the question
        choice1 = models.Choice(text='42', question_id=multiple_question.id)
        choice2 = models.Choice(text='happiness', question_id=multiple_question.id)
        session.add(choice1)
        session.add(choice2)
        session.commit()

        # Creates a poll to be used in the response
        random_poll = models.Poll(creator_id=new_user.id, description='Super Random questions about life', questions=[multiple_question])
        session.add(random_poll)
        session.commit()

        # Create a response
        chosen_choice = choice1
        user_response = models.ResponseChoice(poll_id=random_poll.id, responder_user_id=new_user.id, question_id=multiple_question.id, choice_id=chosen_choice.id)
        session.add(user_response)
        session.commit()

        #Verify that there are relationships
        select_statement = select(models.ResponseChoice)
        response = session.execute(select_statement)
        queried_response = response.first()[0]
        assert queried_response.poll == random_poll
        assert queried_response.responder_user == new_user
        assert queried_response.question == multiple_question
        assert queried_response.choice == chosen_choice

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
