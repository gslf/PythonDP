from abc import ABC, abstractmethod

# This is a complex object (it's not really complex)
class Car:
    def __init__(self):
        self.engine = None
        self.aero = None

    def __str__(self):
        return (f"Car Configurations:\n"
                f"Engine: {self.engine}\n"
                f"Aerodynamics: {self.aero}\n")
    
# This is an abstract builder
class CarBuilder(ABC):
    @abstractmethod
    def build_engine(self): pass

    @abstractmethod
    def build_aero(self): pass

    @abstractmethod
    def get_car(self): pass

# This is a concrete builder implementation
class RacingCarBuilder(CarBuilder):

    def __init__(self):
        self.car = Car()

    def build_engine(self):
        self.car.engine = "V10 turbo racing engine"

    def build_aero(self):
        self.car.aero = "Low drag aero package"

    def get_car(self):
        return self.car

# This is the building director
class Director:
    def __init__(self, builder: CarBuilder):
        self._builder = builder

    # Define the car construction process
    def construct_car(self):
        self._builder.build_engine()
        self._builder.build_aero()

    def get_car(self):
        return self._builder.get_car()
    


# Testing the Builder behaviour
if __name__ == "__main__":

    # Create a builder
    racing_car_builder = RacingCarBuilder()
    # Instanciate a director
    director = Director(racing_car_builder)
    # Build a car
    director.construct_car()
    car = director.get_car()

    print(car)