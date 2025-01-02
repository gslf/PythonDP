# Clean Architecture in Python

Clean Architecture, introduced by Robert C. Martin (Uncle Bob), is a complex software design philosophy that separates concerns through layers, making systems independent of frameworks, databases, UI, and external agencies.

The architecture can be represented in concentric circles, each representing a distinct layer of abstraction. At the center lie the Entities, embodying the core business rules that would exist even if the system were manual. These pure business objects remain untouched by technical concerns, representing the most stable and crucial part of the system.

Surrounding the Entities, we find the Use Cases layer, which orchestrates the flow of data and implements application-specific business rules. This layer brings the static business rules to life, choreographing how the system responds to user actions while remaining independent of technical details like databases or user interfaces.

Moving outward, the Interface Adapters layer serves as a translation boundary. It converts data between the format most convenient for the use cases and entities, and the format required by external agencies such as databases or the web. This crucial layer prevents technical concerns from leaking inward while ensuring that the outside world can effectively communicate with our business logic.

Finally, the outermost layer contains Frameworks and Drivers - the technical details that we tend to think about first but should actually be the most volatile. This includes databases, web frameworks, UI components, and other tools that should be treated as implementation details rather than architectural drivers.

![Clean Architecture Visual Representation](/Architectural/CleanArchitecture/res/clean_architecture_visualization.png)

### Pattern Comparison

| Pattern | Data Management | UI Handling | User Input | Complexity | Learning Curve |
|---------|-----------------|--------------|------------|------------|----------------|
| MVC | Model component | View component | Controller component | Medium | Moderate |
| MVP | Presenter handles model | Passive view | View delegates to presenter | Medium-High | Steep |
| MVVM | ViewModel | View | Two-way data binding | High | Steep |
| Clean Architecture | Use cases & entities | Interface adapters | Controllers | Very High | Very Steep |

Unlike the other patterns in this table, Clean Architecture provides a more comprehensive separation of concerns. Architectures like MVC focuses on separating the user interface from the business logic, Clean Architecture goes further by defining clear boundaries between all system components. Compared to traditional Layered Architecture, Clean Architecture enforces stricter dependency rules and better protects the domain logic.

## Implementation

Let's consider an online bookstore system to understand Clean Architecture in practice. The system needs to manage books, orders, and user interactions.

### Layer Structure:

- **Entities (Core)**
    - Book\
    - Order

- **Use Cases (Application)**
    - CreateOrder
    - AddBook
    - SearchBooks

- **Interface Adapters**
    - BookRepository
    - BookRepository

- **Frameworks & Drivers**
    - Database
    - Web Framework
    - External Services

```python
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
```