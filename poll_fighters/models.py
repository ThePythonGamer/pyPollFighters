from poll_fighters import db
from sqlalchemy import Column, Integer, ForeignKey, TEXT, Table, String
from sqlalchemy.orm import declarative_base, relationship

# To Do:
# Create an Id mixin

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(80), unique=True, nullable=False)
    email = Column(String(120), unique=True, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username

    def __init__(self, username, email):
        self.username = username
        self.email = email

association_table = Table('association', Base.metadata,
    Column('poll_id', Integer, ForeignKey('polls.id')),
    Column('right_id', Integer, ForeignKey('questions.id'))
)

class Poll(Base):
    __tablename__ = 'polls'
    id = Column(Integer, primary_key=True)
    description = Column(TEXT)
    questions = relationship("Question", secondary=association_table)

class Question(Base):
    __tablename__ = 'questions'
    id = Column(Integer, primary_key=True)
    text = Column(TEXT, unique=True)
    
