from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Author(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String)
    birth_date = db.Column(db.String)
    date_of_death = db.Column(db.String)

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    isbn = db.Column(db.Integer)
    title = db.Column(db.String)