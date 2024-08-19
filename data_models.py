from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Author(db.Model):
    __tablename__ = "authors"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String)
    birth_date = db.Column(db.String)
    date_of_death = db.Column(db.String)
    books = db.relationship('Book', backref='author', lazy=True)

class Book(db.Model):
    __tablename__ = "books"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    isbn = db.Column(db.Integer)
    title = db.Column(db.String)
    author_id = db.Column(db.Integer, db.ForeignKey('authors.id'), nullable=False)