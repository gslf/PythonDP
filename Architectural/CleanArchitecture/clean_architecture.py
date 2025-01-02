from dataclasses import dataclass
from typing import List, Optional
from datetime import datetime
from abc import ABC, abstractmethod
from uuid import UUID, uuid4

# =====================================
# ENTITIES
# Core business objects with business rules
# Independent from frameworks and external concerns
# =====================================

@dataclass
class Book:
    id: UUID
    title: str
    author: str
    price: float
    isbn: str

@dataclass 
class Order:
    id: UUID
    books: List[Book]
    total_amount: float
    created_at: datetime

# =====================================
# INTERFACES / USE CASE PORTS
# Abstract interfaces that define repository contracts
# Used by use cases and implemented by external interfaces
# =====================================

class BookRepository(ABC):
    @abstractmethod
    def add(self, book: Book) -> None:
        pass
    
    @abstractmethod
    def get_by_isbn(self, isbn: str) -> Optional[Book]:
        pass

class OrderRepository(ABC):
    @abstractmethod
    def create(self, order: Order) -> None:
        pass

# =====================================
# USE CASES
# Application-specific business rules
# Orchestrates the flow of data and entities
# =====================================

class CreateOrderUseCase:
    def __init__(self, book_repo: BookRepository, order_repo: OrderRepository):
        self.book_repo = book_repo
        self.order_repo = order_repo
    
    def execute(self, isbn_list: List[str]) -> Order:
        books = []
        total_amount = 0.0
        
        # Business logic for creating an order
        for isbn in isbn_list:
            book = self.book_repo.get_by_isbn(isbn)
            if book:
                books.append(book)
                total_amount += book.price
        
        order = Order(
            id=uuid4(),
            books=books,
            total_amount=total_amount,
            created_at=datetime.now()
        )
        self.order_repo.create(order)
        return order

# =====================================
# CONTROLLERS / PRESENTERS
# Handles HTTP requests, CLI commands, or other entry points
# Maps external data format to internal data structures
# =====================================

class BookstoreAPI:
    def __init__(self, book_repo: BookRepository, order_repo: OrderRepository):
        self.order_use_case = CreateOrderUseCase(book_repo, order_repo)
    
    def create_order(self, isbn_list: List[str]) -> Order:
        return self.order_use_case.execute(isbn_list)

# =====================================
# EXTERNAL INTERFACES
# Implements repository interfaces
# Handles database, file system, or external service interactions
# =====================================

class InMemoryBookRepository(BookRepository):
    def __init__(self):
        self.books = {}

    def add(self, book: Book) -> None:
        self.books[book.isbn] = book
    
    def get_by_isbn(self, isbn: str) -> Optional[Book]:
        return self.books.get(isbn)

class InMemoryOrderRepository(OrderRepository):
    def __init__(self):
        self.orders = {}

    def create(self, order: Order) -> None:
        self.orders[order.id] = order

# Example usage showing the flow of control
book_repo = InMemoryBookRepository()
order_repo = InMemoryOrderRepository()

# Sample Book Data
book_title = "1984"
book_isbn = "9786559101139"
book_author = "George Orwell"
book_price = 9.99

book = Book(id=uuid4(), 
            title = book_title, 
            author = book_author, 
            price = book_price, 
            isbn = book_isbn)
book_repo.add(book)

bookstore_api = BookstoreAPI(book_repo, order_repo)
order = bookstore_api.create_order([book_isbn])

print(f"Order ID: {order.id}")
print(f"Total Amount: {order.total_amount}")
print(f"Books in Order: {[book.title for book in order.books]}")