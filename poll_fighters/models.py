from poll_fighters import db
from sqlalchemy import Column, Integer, ForeignKey, TEXT, Table, String
from sqlalchemy.orm import declarative_base, relationship

# To Do:
# Create an Id mixin

class IdMixin:
    id = Column(Integer, primary_key=True)

Base = declarative_base()

class User(Base, IdMixin):
    __tablename__ = 'users'
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

class Poll(Base, IdMixin):
    __tablename__ = 'polls'
    description = Column(TEXT)
    questions = relationship("Question", secondary=association_table)


class Question(Base, IdMixin):
    __tablename__ = 'questions'
    text = Column(TEXT, unique=True)
    question_type_id = Column(Integer, ForeignKey('question_types.id'))
    question_type = relationship("QuestionType")

    def __init__(self, text, question_type_id):
        self.text = text
        self.question_type_id = question_type_id

class QuestionType(Base, IdMixin):
    __tablename__ = 'question_types'
    name = Column(String(20), unique=True, nullable=False)
    description = Column(TEXT)
    
    def __init__(self, name, description=None):
        self.name = name
        self.description = description
