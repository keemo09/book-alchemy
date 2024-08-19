from flask import Flask, render_template, request, redirect, url_for
from data_models import db, Author, Book
import os


app = Flask(__name__)
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data/library.sqlite'

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(basedir, "data", "library.sqlite")}'
db.init_app(app)

with app.app_context():
    db.create_all()


@app.route("/")
def index():
    sorting_choice = request.args.get("sort", "book")
    keyword = request.args.get("keyword")
    search_pattern = f"%{keyword}%" if keyword else "%"

    SORTING_OPTIONS = {"book": Book.query.filter(Book.title.like(search_pattern)).order_by(Book.title).all(), 
                       "author": Book.query.join(Author).filter(Book.title.like(search_pattern)).order_by(Author.name).all()}

    if sorting_choice and sorting_choice in SORTING_OPTIONS:
        books = SORTING_OPTIONS[sorting_choice]
    else:
        books = Book.query.filter(Book.title.like(search_pattern)).all()

    return render_template("home.html", books=books, keyword=keyword)


@app.route("/add_author", methods=["GET", "POST"])
def add_author():
    messages = []
    if request.method == "POST":
        try:
            author = Author(
                name=request.form.get("name"),
                birth_date=request.form.get("birthdate"),
                date_of_death=request.form.get("date_of_death")
            )
            db.session.add(author)
            db.session.commit()
            messages.append("Author successfully created!")
        except Exception:
            messages.append("Something went wrong!")

    return render_template("add_author.html", messages=messages)


@app.route("/add_book", methods=["GET", "POST"])
def add_book():
    messages = []
    try:
        if request.method == "POST":
            book = Book(
                isbn=request.form.get("isbn"),
                title=request.form.get("title"),
                author_id = request.form.get("author_id")
            )
            db.session.add(book)
            db.session.commit()
    except Exception as e:
        messages.append("Something went wrong!")
    
    authors = Author.query.all()
    return render_template("add_book.html", messages=messages, authors=authors)

@app.route("/book/<int:book_id>/delete", methods=["POST"])
def delete_book(book_id):
    book = Book.query.get_or_404(book_id)
    db.session.delete(book)
    db.session.commit()
    return redirect(url_for("index"))


    


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5002)