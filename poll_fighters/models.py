from poll_fighters import db

class Base(db.Model):
    pass

class User(Base):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username

association_table = db.Table('association', Base.metadata,
    Column('poll_id', Integer, ForeignKey('polls.id')),
    Column('right_id', Integer, ForeignKey('questions.id'))
)

class Poll(Base):
    __tablename__ = 'polls'
    id = db.Column(db.Integer, primary_key=True)
    description = id.Column(db.TEXT)
    questions = relationship("Question", secondary=association_table,back_populates="parents")

class Question(Base):
    __tablename__ = 'questions'
    id = db.Column(db.Integer, primary_key=True)
    text = id.Column(db.TEXT, unique=True)
    
