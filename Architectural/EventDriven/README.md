# Event-Driven Architecture in Python

Event-Driven Architecture (EDA) is a software design pattern where the flow of the application is determined by events such as user actions, sensor outputs, or system messages. In this architecture, events are produced, detected, consumed, and reacted to in real-time. This creates a highly decoupled system where components communicate through events rather than direct method calls.

An Event-Driven Architecture consists of four fundamental components:

- **Event Producers:** Event Producers are components responsible for generating events. These events can arise from user actions, system changes, or external services. Producers create and publish events to the event bus, but have no knowledge of event consumers.
- **Event Bus (Message Broker):** The Event Bus, also known as message broker, acts as the central nervous system for Event-Driven Architecture (EDA). It receives events from producers and routes them to consumers, managing event queues and ensuring reliable delivery. Common implementations include Apache Kafka, RabbitMQ, and Redis, which can handle various messaging patterns such as pub/sub and point-to-point.
- **Event Consumers:** Event Consumers are components that react to events. They subscribe to specific types of events and process them according to business logic. They can operate synchronously or asynchronously and, in some cases, may also produce new events in response to received ones.
- **Event Store:** The Event Store is an optional but common component that maintains a record of all events. This tool enables system recovery and event replay, proving useful for audit logs and debugging. It also supports the event sourcing pattern, facilitating event management and analysis over time.

![Event Driven Architecture Visual Representation](/Architectural/EventDriven/res/event_driven_visualization.png)

## Implementation
Let's consider an e-commerce platform's order processing system. When a customer places an order, several actions need to occur:

- Inventory must be updated
- Payment must be processed
- Confirmation email must be sent
- Shipping department must be notified
- Analytics must be updated

Instead of handling these tasks in a monolithic sequence, EDA processes them as independent reactions to the "OrderPlaced" event. This allows each service to operate independently and ensures system resilience - if the email service fails, it doesn't affect inventory updates.

```python
from dataclasses import dataclass
from typing import Any, Dict, List, Callable
from datetime import datetime
import time

@dataclass
class OrderPlacedEvent:
    order_id: str
    customer_id: str
    items: List[Dict[str, int]]
    timestamp: datetime

class EventBus:
    def __init__(self):
        self._subscribers: Dict[str, List[Callable]] = {}
    
    def subscribe(self, event_type: str, handler: Callable) -> None:
        if event_type not in self._subscribers:
            self._subscribers[event_type] = []
        self._subscribers[event_type].append(handler)
    
    def publish(self, event_type: str, event: Any) -> None:
        if event_type in self._subscribers:
            for handler in self._subscribers[event_type]:
                handler(event)

class InventoryService:
    def update_inventory(self, event: OrderPlacedEvent) -> None:
        print(f"Updating inventory for order {event.order_id}")
        time.sleep(1)  # Simulate processing time
        print("Inventory updated successfully")

class PaymentService:
    def process_payment(self, event: OrderPlacedEvent) -> None:
        print(f"Processing payment for order {event.order_id}")
        time.sleep(0.5)  # Simulate processing time
        print("Payment processed successfully")

class NotificationService:
    def send_confirmation(self, event: OrderPlacedEvent) -> None:
        print(f"Sending confirmation email for order {event.order_id}")
        time.sleep(0.3)  # Simulate processing time
        print("Confirmation email sent")

def main():
    # Initialize event bus and services
    event_bus = EventBus()
    inventory_service = InventoryService()
    payment_service = PaymentService()
    notification_service = NotificationService()
    
    # Register event handlers
    event_bus.subscribe("order_placed", inventory_service.update_inventory)
    event_bus.subscribe("order_placed", payment_service.process_payment)
    event_bus.subscribe("order_placed", notification_service.send_confirmation)
    
    # Create and publish an order event
    order_event = OrderPlacedEvent(
        order_id="12345",
        customer_id="USER001",
        items=[{"item_id": "PROD1", "quantity": 2}],
        timestamp=datetime.now()
    )
    
    event_bus.publish("order_placed", order_event)

if __name__ == "__main__":
    main()
```