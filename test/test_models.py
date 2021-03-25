from poll_fighters import models
from sqlalchemy import select, func, create_engine
from sqlalchemy.orm import sessionmaker

# To Do:
# Clear the database at the end of each test
# Add session fixture

def test_user_initilized_empty():
    statement = select(func.count()).select_from(models.User)
    engine = create_engine('sqlite:////tmp/apptests.db')
    Session = sessionmaker(engine)
    session = Session()
    models.Base.metadata.create_all(engine)
    response = session.execute(statement)
    #assert response.scalar() == 0
    response.scalar().should.be.equal(0)

def test_add_user():
    statement = select(func.count()).select_from(models.User)
    engine = create_engine('sqlite:////tmp/apptests.db')
    Session = sessionmaker(engine)
    session = Session()
    test_user = models.User('testuser', 'test@email.com')
    session.add(test_user)
    session.commit()
    session.execute(statement).scalar().should.be.equal(1)
    