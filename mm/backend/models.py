# backend/models.py

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'user_data'
    __table_args__ = {'schema': 'user'}
    id = db.Column(db.Integer, primary_key=True)
    # user_id = db.Column(db.Integer, unique=True,  autoincrement=True)
    username = db.Column(db.String(50), unique=False, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

    def __init__(self,  username, email, password):
        self.username = username
        self.email = email
        self.password = password

class Income(db.Model):
    __tablename__ = 'income'
    __table_args__ = {'schema': 'user'}
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer,  nullable=False)
    amount = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(200), nullable=False)
    date = db.Column(db.String(10), nullable=False)
    
    def as_dict(self):
        return {
            'id': self.id,
            'amount': self.amount,
            'category': self.category,
            'description': self.description,
            'date': self.date,
            'user_id': self.user_id
        }



class Expense(db.Model):
    __tablename__ = 'expense'
    __table_args__ = {'schema': 'user'}
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer,  nullable=False)
    amount = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(255), nullable=True)
    description = db.Column(db.String(255), nullable=True)
    date = db.Column(db.String(10), nullable=False)  
    
    def as_dict(self):
        return {
            'id': self.id,
            'amount': self.amount,
            'category': self.category,
            'description': self.description,
            'date': self.date,
            'user_id': self.user_id
        }


class Budget(db.Model):
    __tablename__ = 'budget'
    __table_args__ = {'schema': 'user'}
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer,  nullable=False)
    amount = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(255), nullable=True)
 
    def as_dict(self):
        return {
            'id': self.id,
            'amount': self.amount,
            'category': self.category,
            'description': self.description,
            'user_id': self.user_id
        }