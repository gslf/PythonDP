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