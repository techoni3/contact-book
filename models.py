from flask import Flask
from sqlalchemy import Column, Integer, String
from flask_sqlalchemy import SQLAlchemy
from config import SQLALCHEMY_DATABASE_URI
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Contact(db.Model):
    __tablename__ = 'Contacts'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    email_id = Column(String(255), nullable=False, unique=True)
    phone = Column(String(20), nullable=False)

    def __repr__(self):
        return f"<Contact {self.name}:{self.phone}>"

    def __init__(self, name, phone, email):
        self.name = name
        self.phone = phone
        self.email_id = email
