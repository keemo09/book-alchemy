# Book-Alchemy
A web application for managing books and authors in a library efficiently, built with Flask and SQLite.

## Installation

1. Clone the repository:
   git clone https://github.com/username/MyProjectName.git](https://github.com/keemo09/book-alchemy.git
   
2. Install dependencies:
   pip install -r requirements.txt

3. Run the application
   uvicorn app.main:app --reload

## **Usage**

After starting the application, open your browser and navigate to `http://127.0.0.1:5002` to access the web application.

### **API Endpoints**

- **`GET /`**: Fetch all books with the option to sort by title or author.
- **`POST /add_author`**: Add a new author (requires a name, birthdate, and date of death).
- **`POST /add_book`**: Add a new book (requires ISBN, title, and author ID).
- **`GET /book/<int:book_id>`**: Fetch the details of a specific book by ID.
- **`GET /author/<int:author_id>`**: Fetch the details of a specific author by ID.
- **`POST /book/<int:book_id>/delete`**: Delete a book by its ID.



## Contributing

Contributions are welcome! Please follow the [contribution guidelines](CONTRIBUTING.md).




## Contact

Created by [keemo09](https://github.com/keemo09) - feel free to reach out!
