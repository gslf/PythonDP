from dataclasses import dataclass
from typing import List, Optional

# MODEL
@dataclass
class Book:
    title: str
    author: str
    isbn: str
    id: Optional[int] = None

class BookModel:
    def __init__(self):
        self._books: List[Book] = []
    
    def add_book(self, book: Book) -> None:
        """Add a new book to the database"""
        book.id = len(self._books) + 1
        self._books.append(book)
    
    def get_books(self) -> List[Book]:
        """Retrieve all books"""
        return self._books.copy()
    
    def find_book(self, isbn: str) -> Optional[Book]:
        """Find a book by ISBN"""
        return next((book for book in self._books if book.isbn == isbn), None)

# VIEW
class BookView:
    def display_books(self, books: List[Book]) -> None:
        """Display all books in a formatted way"""
        print("\n=== Library Books ===")
        for book in books:
            print(f"ID: {book.id}, Title: {book.title}, Author: {book.author}, ISBN: {book.isbn}")
    
    def get_book_input(self) -> tuple[str, str, str]:
        """Get book details from user"""
        title = input("Enter book title: ")
        author = input("Enter book author: ")
        isbn = input("Enter book ISBN: ")
        return title, author, isbn

# CONTROLLER
class BookController:
    def __init__(self, model: BookModel, view: BookView):
        self.model = model
        self.view = view
    
    def add_book(self) -> None:
        """Handle the process of adding a new book"""
        title, author, isbn = self.view.get_book_input()
        book = Book(title=title, author=author, isbn=isbn)
        self.model.add_book(book)
    
    def show_books(self) -> None:
        """Display all books through the view"""
        books = self.model.get_books()
        self.view.display_books(books)

# Usage Example
def main():
    model = BookModel()
    view = BookView()
    controller = BookController(model, view)
    
    # Add some sample books
    controller.add_book()
    controller.add_book()
    
    # Display all books
    controller.show_books()

if __name__ == "__main__":
    main()