from sqlalchemy.sql.expression import column
from poll_fighters import db
from sqlalchemy import Column, Integer, ForeignKey, TEXT, Table, String
from sqlalchemy.orm import declarative_base, declarative_mixin, declared_attr, relationship

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
    choices = relationship('Choice', backref='questions')

    def __init__(self, text, question_type_id):
        self.text = text
        self.question_type_id = question_type_id

    def __eq__(self, other):
        return other and self.text == other.text and self.question_type_id == other.question_type_id or False

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
    question_id = Column(Integer, ForeignKey('questions.id'))

    def __init__(self, text, question_id):
        self.text = text
        self.question_id = question_id

@declarative_mixin
class Response(IdMixin):
    @declared_attr
    def poll_id(self):
        return Column(Integer, ForeignKey('polls.id'))

    @declared_attr
    def poll(self):
        return relationship('Poll')

    @declared_attr
    def responder_user_id(self):
        return Column(Integer, ForeignKey('users.id'))
    
    @declared_attr
    def responder_user(self):
        return relationship('User')

    @declared_attr
    def question_id(self):
        return Column(Integer, ForeignKey('questions.id'))

    @declared_attr
    def question(self):
        return relationship('Question')
        

class ResponseOpen(Base, Response): 
    __tablename__ = 'poll_response_open'
    open_response = Column(TEXT)

    def __init__(self, open_response, poll_id, responder_user_id, question_id):
        self.open_response = open_response
        self.poll_id = poll_id
        self.responder_user_id = responder_user_id
        self.question_id = question_id

class ResponseChoice(Base, Response):
    __tablename__ = 'poll_response_choice'
    choice_id = Column(Integer, ForeignKey('choices.id'))
    choice = relationship(Choice)

    def __init__(self, poll_id, responder_user_id, question_id):
        self.poll_id = poll_id
        self.responder_user_id = responder_user_id
        self.question_id = question_id