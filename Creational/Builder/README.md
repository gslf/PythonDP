# The Builder design pattern

The Builder pattern is used to construct a complex object step-by-step. The components of a builder are:

- **Object**: a complex obkect that consiste of multiple components.
- **Builder**: an abstract interface that declares the construction steps.
- **Concrete Builders**: implementations of the builder interface, that create a specific variation of the product. It keeps track of the product it creates and provides a method to retrieve it.
- **Director**: who decides how to build the object step by step. The director takes a concrete builder and manages its workflow.

The Builder pattern hides the creation logic of a complex object, meaning the client code doesn't need to be aware of the individual construction steps. Instead, it simply interacts with the Director to obtain a fully assembled instance. This is an example of encapsulation.

This is a visual representation of this pattern:

![Prototype Pattern Visual Representation](/Prototype/res/prototype_visualization.png)

## Implementation
This is an implementation of the builder pattern:
```python
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
```