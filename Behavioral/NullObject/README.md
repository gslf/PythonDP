# Null Object Design PAttern in Python

The Null Object pattern is a behavioral design pattern that provides an elegant solution to **handle null references** in object-oriented programming. Instead of using null references or checking for nulls throughout the code, this pattern introduces a special "do nothing" object that implements the same interface as the real object but exhibits neutral behavior.

The pattern consists of three main components:

- An abstract class or interface defining the behavior
- A concrete implementation providing the real functionality
- A null object implementation providing neutral behavior

The null object is designed to handle the absence of a real object gracefully, typically by doing nothing or returning neutral values.

![Null Object Pattern Visual Representation](/Behavioral/NullObject/res/null_object_visualization.png)


## Implementation

Consider a company's notification system that sends messages to employees. Some employees might be on vacation or have left the company, requiring a different handling of notifications. Instead of checking if an employee exists before sending each notification, we can use a null object to handle inactive employees automatically.

When an employee goes on vacation or leaves, instead of removing them from the system or checking their status repeatedly, we replace their normal notification handler with a null object that silently discards messages.

```python
from abc import ABC, abstractmethod
from typing import List

class NotificationHandler(ABC):
    """Abstract base class defining the notification handling interface"""
    
    @abstractmethod
    def send_message(self, message: str) -> None:
        """Send a message to the employee"""
        pass
    
    @abstractmethod
    def get_delivery_status(self) -> str:
        """Get the status of message delivery"""
        pass

class ActiveEmployeeHandler(NotificationHandler):
    """Handles notifications for active employees"""
    
    def __init__(self, employee_name: str, email: str):
        self.employee_name = employee_name
        self.email = email
        self.messages: List[str] = []
    
    def send_message(self, message: str) -> None:
        # In a real system, this would send an email
        self.messages.append(message)
        print(f"Message sent to {self.employee_name} at {self.email}: {message}")
    
    def get_delivery_status(self) -> str:
        return f"Active: {len(self.messages)} messages delivered"

class NullEmployeeHandler(NotificationHandler):
    """Null object for handling inactive employee notifications"""
    
    def __init__(self, employee_name: str):
        self.employee_name = employee_name
    
    def send_message(self, message: str) -> None:
        # Silently discard the message
        pass
    
    def get_delivery_status(self) -> str:
        return "Inactive: no messages delivered"


# EXAMPLE USAGE
# Create notification handlers for different employees
active_employee = ActiveEmployeeHandler("John Doe", "john@company.com")
inactive_employee = NullEmployeeHandler("Jane Smith")

# Send notifications without checking employee status
active_employee.send_message("Team meeting at 2 PM")
inactive_employee.send_message("Team meeting at 2 PM")

# Check delivery status
print(active_employee.get_delivery_status())
print(inactive_employee.get_delivery_status())

```