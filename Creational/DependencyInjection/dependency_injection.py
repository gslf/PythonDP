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
