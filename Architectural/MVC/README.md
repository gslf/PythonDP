# Model-View-Controller (MVC) pattern

The Model-View-Controller (MVC) is an architectural pattern revolves around separation of concerns. MVC separates an application into three main logical components: Model, View, and Controller. 

By dividing the application into distinct components, we achieve:

- Modularity: Changes to one component don't affect others
- Maintainability: Easier debugging and feature implementation
- Parallel Development: Teams can work simultaneously on different components
- Code Reusability: Components can be reused across applications
- Testability: Individual components can be tested in isolation


![Modal View Controller Visual Representation](/Architectural/MVC/res/mvc_visualization.png)

### Pattern Comparison

| Pattern | Data Management | UI Handling | User Input | Complexity | Learning Curve |
|---------|-----------------|--------------|------------|------------|----------------|
| MVC | Model component | View component | Controller component | Medium | Moderate |
| MVP | Presenter handles model | Passive view | View delegates to presenter | Medium-High | Steep |
| MVVM | ViewModel | View | Two-way data binding | High | Steep |
| Clean Architecture | Use cases & entities | Interface adapters | Controllers | Very High | Very Steep |


## Implementation

Let's consider a library management system to understand MVC:

#### Model: Book class containing data and business logic
- Book properties (title, author, ISBN)
- Database operations
- Business rules validation

#### View: User interface showing books
- Book list display
- Search interface
- Add/Edit book forms

#### Controller: Handles user actions
- Process search requests
- Validate and route add/edit operations
- Coordinate model updates and view refreshes


```python
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
```

This pattern makes it easy to:

- Replace the console-based view with a GUI without changing other components
- Add new features by extending the controller
- Modify data storage without affecting the user interface
- Test components independently