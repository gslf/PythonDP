# The Facade Design Pattern

The Facade Design Pattern is a structural pattern that offers a **simplified interface** to a complex system of classes, a subsystem, or a library. It "facilitates" interaction by creating a higher-level interface that abstracts the functionality of more complicated components.

You can picture it as the front desk at a hotel. As a guest, you interact with the front desk rather than directly dealing with housekeeping, restaurant services, or maintenance. The front desk is the facade, providing a simple point of contact to handle your various requests, hiding the complexities of the internal departments. 

![Facade Pattern Visual Representation](/Facade/res/facade_visualization.png)

The Facade pattern acts as a gateway, an **abstraction layer** between the client code and the underlying subsystems. This reduces the cognitive load for developers who only need to understand and interact with the simplified interface, instead of internal intricacies. It’s a way of reducing informational entropy and creating cognitive clarity.

## Implementation
This implementation demonstrates a hotel front desk system with multiple components (such as housekeeping, restaurant, and maintenance), and the Facade helps manage the entire experience for a guest who just wants to request services easily.

```python
class Housekeeping:
    def clean_room(self, room_number):
        print(f"Housekeeping is cleaning room {room_number}")

    def request_towels(self, room_number):
        print(f"Delivering fresh towels to room {room_number}")

class Restaurant:
    def order_food(self, room_number, food_item):
        print(f"Ordering '{food_item}' for room {room_number}")

    def reserve_table(self):
        print("A table has been reserved at the restaurant")

class Maintenance:
    def fix_issue(self, room_number, issue):
        print(f"Maintenance is fixing '{issue}' in room {room_number}")

    def check_systems(self):
        print("Maintenance is performing a routine system check")

# The Facade Class
class FrontDeskFacade:
    def __init__(self, housekeeping: Housekeeping, restaurant: Restaurant, maintenance: Maintenance):
        self.housekeeping = housekeeping
        self.restaurant = restaurant
        self.maintenance = maintenance

    def request_cleaning(self, room_number):
        print("Guest requested room cleaning...")
        self.housekeeping.clean_room(room_number)

    def request_towels(self, room_number):
        print("Guest requested fresh towels...")
        self.housekeeping.request_towels(room_number)

    def order_food(self, room_number, food_item):
        print("Guest requested food order...")
        self.restaurant.order_food(room_number, food_item)

    def reserve_table(self):
        print("Guest requested a table reservation...")
        self.restaurant.reserve_table()

    def report_issue(self, room_number, issue):
        print("Guest reported an issue...")
        self.maintenance.fix_issue(room_number, issue)
        # Notifying housekeeping to check the room condition after maintenance
        self.housekeeping.clean_room(room_number) 

# Client code
if __name__ == "__main__":
    housekeeping = Housekeeping()
    restaurant = Restaurant()
    maintenance = Maintenance()
    
    # Create the Facade
    front_desk = FrontDeskFacade(housekeeping, restaurant, maintenance)
    
    # Interact with the simplified interface
    front_desk.request_cleaning(101)
    front_desk.order_food(101, "Pasta")
    front_desk.report_issue(101, "leaky faucet")
```

The Facade Design Pattern is a tool for simplifying complex systems and providing an abstraction layer. By providing an intuitive interface, the Facade pattern allows developers to create more maintainable, readable, and scalable code. As systems grow in complexity, this pattern can be instrumental in helping developers stay sane and productive.