# Thread Pool - Concurrency in Python
The **Thread Pool** pattern us used in **concurrent programming** go manage a collection of pre-initialized, reusable threads stands ready to execute tasks. Instead of creating new threads for each task, which can be resource-intensive, the pattern maintains a "pool" of worker threads that can be recycled for multiple tasks throughout the application's lifecycle.

The core philosophy behind thread pools stems from the "resource reuse" principle. Creating and destroying threads involves significant overhead in terms of time and system resources.

**A thread pool consists of three main components:**

- Task Queue - Stores incoming tasks waiting to be processed
- Worker Threads - The actual threads that execute the tasks
- Thread Pool Manager - Coordinates task distribution and thread lifecycle

![Thread Pool Visual Representation](/Concurrency/ThreadPool/res/thread_pool_visualization.png)

## Implementation
Imagine a restaurant kitchen with four chefs (worker threads) and a stack of order tickets (task queue). Instead of hiring a new chef for each incoming order (creating new threads), the same four chefs handle all orders throughout the day. When an order arrives, it goes into the ticket stack. Any available chef takes the next ticket and prepares that order. If all chefs are busy, new orders wait in the stack until a chef becomes available.

This is an implmentation to emulate this restaurant scenario:

```python
from concurrent.futures import ThreadPoolExecutor
from typing import List
from dataclasses import dataclass
import threading
import time

@dataclass
class Order:
    """Represents a food order in our restaurant"""
    id: int
    dish_name: str
    preparation_time: float

class RestaurantThreadPool:
    def __init__(self, num_chefs: int):
        """Initialize the restaurant thread pool with a specific number of chefs"""
        self.executor = ThreadPoolExecutor(max_workers=num_chefs, thread_name_prefix="Chef")
        self.orders_prepared = 0
        self.lock = threading.Lock()

    def prepare_dish(self, order: Order) -> str:
        """Simulate dish preparation by a chef (worker thread)"""
        chef_name = threading.current_thread().name
        print(f"{chef_name} started preparing {order.dish_name} (Order #{order.id})")
        
        # Simulate cooking time
        time.sleep(order.preparation_time)
        
        with self.lock:
            self.orders_prepared += 1
        
        return f"{chef_name} completed {order.dish_name} (Order #{order.id})"

    def process_orders(self, orders: List[Order]) -> None:
        """Process multiple orders concurrently"""
        # Submit all orders to the thread pool
        futures = [
            self.executor.submit(self.prepare_dish, order)
            for order in orders
        ]
        
        # Wait for all orders to complete and print results
        for future in futures:
            print(future.result())

    def shutdown(self) -> None:
        """Close the restaurant (shutdown the thread pool)"""
        self.executor.shutdown()
        print(f"Restaurant closed. Total orders prepared: {self.orders_prepared}")

############################
# Example usage

# Create sample orders
sample_orders = [
    Order(1, "Pizza", 2.0),
    Order(2, "Pasta", 1.5),
    Order(3, "Salad", 1.0),
    Order(4, "Steak", 3.0),
    Order(5, "Soup", 1.0),
    Order(6, "Dessert", 1.5)
]

# Initialize restaurant with 4 chefs
restaurant = RestaurantThreadPool(num_chefs=4)

# Process all orders
restaurant.process_orders(sample_orders)

# Close restaurant
restaurant.shutdown()
```
