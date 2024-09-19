from flask import Flask, render_template, request, redirect, url_for
from data_models import db, Author, Book
import os


app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config["SQLALCHEMY_DATABASE_URI"] = (
    f'sqlite:///{os.path.join(basedir, "data", "library.sqlite")}'
)
db.init_app(app)

with app.app_context():
    db.create_all()


@app.route("/")
def index():
    """
    Get a optimal query argument for sort (default is book) and keyword.
    Returns a list view template with the listed books.
    """
    sorting_choice = request.args.get("sort", "book")
    keyword = request.args.get("keyword")
    search_pattern = f"%{keyword}%" if keyword else "%"

    # Dispatcher for the specific Sorting query
    # SORTING_OPTIONS = {
    #     "book": Book.query.filter(Book.title.like(search_pattern))
    #     .order_by(Book.title)
    #     .all(),
    #     "author": Book.query.join(Author)
    #     .filter(Book.title.like(search_pattern))
    #     .order_by(Author.name)
    #     .all(),
    # }
    SORTING_OPTIONS = {
        "book": lambda: Book.query.filter(Book.title.like(search_pattern))
        .order_by(Book.title)
        .all(),
        "author": lambda: Book.query.join(Author)
        .filter(Book.title.like(search_pattern))
        .order_by(Author.name)
        .all(),
    }

    # Checks if a sorting choice value is given
    # If sorting choice given call sorting dispatcher with search pattern.
    if sorting_choice and sorting_choice in SORTING_OPTIONS:
        books = SORTING_OPTIONS[sorting_choice]()
    else:
        books = Book.query.filter(Book.title.like(search_pattern)).all()

    return render_template("home.html", books=books, keyword=keyword)


@app.route("/add_author", methods=["GET", "POST"])
def add_author():
    """
    If method GET retruns a form with fields: name, birthdate, date_of_death.
    If method POST fetches form data and create a new db record for Author.

    """
    messages = []  # List for messages
    if request.method == "POST":
        try:
            # Create a new Author record and add it and commit it to session.
            author = Author(
                name=request.form.get("name"),
                birth_date=request.form.get("birthdate"),
                date_of_death=request.form.get("date_of_death"),
            )
            db.session.add(author)
            db.session.commit()
            messages.append("Author successfully created!")

        except Exception:
            messages.append("Something went wrong!")

    return render_template("add_author.html", messages=messages)


@app.route("/add_book", methods=["GET", "POST"])
def add_book():
    """
    If method GET retruns a form with fields: isbn, title, author_id.
    If method POST fetches form data and create a new db record for Book.

    """
    messages = []  # List for messages
    try:
        # Create a new Book record and add it and commit it to session.
        if request.method == "POST":
            book = Book(
                isbn=request.form.get("isbn"),
                title=request.form.get("title"),
                author_id=request.form.get("author_id"),
            )
            db.session.add(book)
            db.session.commit()
            messages.append("Author successfully created!")
    except Exception as e:
        messages.append("Something went wrong!")

    authors = Author.query.all()
    return render_template("add_book.html", messages=messages, authors=authors)


@app.route("/book/<int:book_id>/delete", methods=["POST"])
def delete_book(book_id):
    """
    Get a book_id as a url argument.
    Deletes the Book record with the book_id and redirect to index.
    """
    book = Book.query.get_or_404(book_id)
    db.session.delete(book)
    db.session.commit()
    return redirect(url_for("index"))


@app.route("/book/<int:book_id>")
def get_book(book_id):
    """
    Get a book_id as a url argument.
    Returns the rendered template with book details.
    """
    book = Book.query.get_or_404(book_id)
    return render_template("book_details.html", book=book)


@app.route("/author/<int:author_id>")
def get_author(author_id):
    """
    Get a author_id as a url argument.
    Returns the rendered template with author details.
    """
    author = Author.query.get_or_404(author_id)
    return render_template("author_details.html", author=author)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5002)
