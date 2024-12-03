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