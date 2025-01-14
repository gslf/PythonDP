from dataclasses import dataclass
from typing import Optional, List, Dict
from abc import ABC, abstractmethod

# Entity class representing a book
@dataclass
class Book:
    id: Optional[int]
    title: str
    author: str
    isbn: str

# DAO Interface
class BookDAO(ABC):
    @abstractmethod
    def get_by_id(self, book_id: int) -> Optional[Book]:
        pass
    
    @abstractmethod
    def get_all(self) -> List[Book]:
        pass
    
    @abstractmethod
    def create(self, book: Book) -> Book:
        pass
    
    @abstractmethod
    def update(self, book: Book) -> bool:
        pass
    
    @abstractmethod
    def delete(self, book_id: int) -> bool:
        pass

# In-Memory DAO Implementation
class InMemoryBookDAO(BookDAO):
    def __init__(self):
        # Simple dictionary acting as our in-memory database
        self._books: Dict[int, Book] = {}
        self._next_id: int = 1
    
    def get_by_id(self, book_id: int) -> Optional[Book]:
        return self._books.get(book_id)
    
    def get_all(self) -> List[Book]:
        return list(self._books.values())
    
    def create(self, book: Book) -> Book:
        # Assign new ID and store the book
        book.id = self._next_id
        self._books[self._next_id] = book
        self._next_id += 1
        return book
    
    def update(self, book: Book) -> bool:
        if book.id in self._books:
            self._books[book.id] = book
            return True
        return False
    
    def delete(self, book_id: int) -> bool:
        if book_id in self._books:
            del self._books[book_id]
            return True
        return False
    
    

##########################################
# Example usage and testing

# Initialize the DAO
book_dao = InMemoryBookDAO()

# Create some books
book1 = Book(None, "The Hobbit", "J.R.R. Tolkien", "978-0547928227")
book2 = Book(None, "1984", "George Orwell", "978-0451524935")

# Test create operation
created_book1 = book_dao.create(book1)
created_book2 = book_dao.create(book2)
print(f"Created books: {book_dao.get_all()}")

# Test get operation
fetched_book = book_dao.get_by_id(1)
print(f"Fetched book: {fetched_book}")

# Test update operation
updated_book = Book(1, "The Hobbit", "J.R.R. Tolkien", "978-0547928227-updated")
book_dao.update(updated_book)
print(f"After update: {book_dao.get_by_id(1)}")

# Test delete operation
book_dao.delete(2)
print(f"After deletion: {book_dao.get_all()}")
