from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://appuser:apppassword@localhost:5432/appdb'
db = SQLAlchemy(app)
