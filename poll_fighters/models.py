from poll_fighters import db
from sqlalchemy import Column, Integer, ForeignKey, TEXT, Table, String
from sqlalchemy.orm import declarative_base, relationship

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
    Column('question_id', Integer, ForeignKey('questions.id'))
)

class Poll(Base, IdMixin):
    __tablename__ = 'polls'
    description = Column(TEXT)
    questions = relationship("Question", secondary=association_table)

    def __init__(self, description, questions=None):
        self.description = description
        if questions != None:
            self.questions = questions


class Question(Base, IdMixin):
    __tablename__ = 'questions'
    text = Column(TEXT, unique=True)
    question_type_id = Column(Integer, ForeignKey('question_types.id'))
    question_type = relationship("QuestionType")

    def __init__(self, text, question_type_id):
        self.text = text
        self.question_type_id = question_type_id

    def __eq__(self, other):
        return self.text == other.text and self.question_type_id == other.question_type_id

    def __ne__(self, other):
        return not self.__eq__(other)

class QuestionType(Base, IdMixin):
    __tablename__ = 'question_types'
    name = Column(String(20), unique=True, nullable=False)
    description = Column(TEXT)
    constant_types = ['Multiple', 'Open', 'Radio']

    def __init__(self, name, description=None):
        self.name = name
        self.description = description

class Choice(Base, IdMixin):
    __tablename__ = 'choices'
    text = Column(String(35))

# class Responses(Base, IdMixin): 
#     __tablename__ = 'poll_responses'
#     poll_id = Column(Integer, ForeignKey('polls.id'))
#     responder_user_id = Column(Integer, ForeignKey('users.id'))
#     question_id = Column(Integer, ForeignKey('questions.id'))
#     open_response = Column(TEXT, nullable=True)
#     choice_id = Column(Integer, ForeignKey('choices.id'), nullable=True)

class Response(IdMixin):
    poll_id = Column(Integer, ForeignKey('polls.id'))
    poll = relationship(Poll)
    responder_user_id = Column(Integer, ForeignKey('users.id'))
    responder_user = relationship(User)
    question_id = Column(Integer, ForeignKey('questions.id'))
    question = relationship(Question)

class ResponseOpen(Base, Response): 
    __tablename__ = 'poll_response_open'
    open_response = Column(TEXT)

class ResponseChoice(Base, Response):
    __tablename__ = 'poll_response_choice'
    choice_id = Column(Integer, ForeignKey('choices.id'))
    choice = relationship(Choice)

# To Do: 
# Write two new models:
# 1. the choices for multiple choice
# 2. the responses from the users 
# each record in the table of responses would have what poll was it, who responded, what question, what answer
# could be in a single model or multiple models with relationships