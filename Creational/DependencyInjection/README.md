# Dependency Injection pattern in Python
Dependency Injection (DI) is a design pattern that implements **Inversion of Control (IoC)** for managing dependencies between components in software applications.

The main philosophy behind DI is the separation of concerns and the single responsibility principle. Instead of components creating or finding their dependencies, they declare what they need, and a separate entity (often called a container or injector) provides these dependencies. 

The DI pattern involves three main components:

- **The Client (dependent class)** is the component that requires certain dependencies to function.
- **The Service (dependency)** is the functionality or resource that the client needs.
- **The Injector (container)** is responsible for creating instances of the service and injecting them into the client.

![Dependency Injection Visual Representation](/Creational/DependencyInjection/res/dependency_injection_visualization.png)

## Implementation 
Let's consider a practical example of a notification system for an e-commerce platform. Without DI, a class might directly instantiate its notification methods:

```python
class OrderProcessor:
    def __init__(self):
        self.email_service = EmailService()  # Hard-coded dependency
        self.sms_service = SMSService()      # Hard-coded dependency
    
    def process_order(self, order):
        # Process order...
        self.email_service.send("Order processed")
        self.sms_service.send("Order processed")
```

This implementation is tightly coupled and hard to test. What if we want to use different notification services or mock them for testing? Here's where DI comes in:

```python
from typing import Protocol
from dataclasses import dataclass

# Define the notification protocol
class NotificationService(Protocol):
    def send(self, message: str) -> None:
        ...

# Concrete implementations
class EmailService:
    def send(self, message: str) -> None:
        print(f"Sending email: {message}")

class SMSService:
    def send(self, message: str) -> None:
        print(f"Sending SMS: {message}")

# Order data structure
@dataclass
class Order:
    id: str
    amount: float
    customer_email: str

# The client class with injected dependencies
class OrderProcessor:
    def __init__(self, notification_services: list[NotificationService]) -> None:
        """
        Initialize OrderProcessor with injected notification services.
        
        Args:
            notification_services: List of services implementing NotificationService protocol
        """
        self.notification_services = notification_services

    def process_order(self, order: Order) -> None:
        """
        Process an order and notify through all available services.
        
        Args:
            order: Order instance to process
        """
        # Simulate order processing
        print(f"Processing order {order.id}")
        
        # Notify through all available services
        for service in self.notification_services:
            service.send(f"Order {order.id} processed for ${order.amount}")


##############################
# Example Usage

# Create services
email_service = EmailService()
sms_service = SMSService()

# Create processor with injected dependencies
processor = OrderProcessor([email_service, sms_service])

# Create and process an order
order = Order(id="12345", amount=99.99, customer_email="customer@example.com")
processor.process_order(order)

```