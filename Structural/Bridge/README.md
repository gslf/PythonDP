# The Bridge Design Pattern

The Bridge pattern helps solve the problem of multiplying code by avoiding tight coupling between abstraction and implementation. This pattern separates abstraction and implementation into different class hierarchies. The abstraction holds a reference to the implementation, allowing each to vary independently. The abstraction defines the high-level behavior, while the implementor provides the operational details. This decoupling prevents subclass explosion and ensures a modular, extensible architecture.

![Bridge Pattern Visual Representation](/Bridge/res/bridge_visualization.png)


## Implementation
This is an implementation of the Bridge pattern:

```python
# Implementation of the Bridge Design Pattern in a Motorsport context.
# In this example, the Bridge Pattern separates the abstraction (Vehicle) from its implementation details (Tyre).
# Different types of vehicles (e.g., Formula 1 Car, Rally Car) can use different tyres, providing flexibility.

from abc import ABC, abstractmethod

# Abstraction Layer
class Vehicle(ABC):
    def __init__(self, tyre):
        self.tyre = tyre

    @abstractmethod
    def description(self):
        pass

# Refined Abstractions
class FormulaOneCar(Vehicle):
    def __init__(self, tyre):
        super().__init__(tyre)

    def description(self):
        return f"Formula 1 Car with {self.tyre.specifications()}"

class RallyCar(Vehicle):
    def __init__(self, tyre):
        super().__init__(tyre)

    def description(self):
        return f"Rally Car with {self.tyre.specifications()}"

# Implementation Layer
class Tyre(ABC):
    @abstractmethod
    def specifications(self):
        pass

# Concrete Implementations of Tyre
class SlickTyre(Tyre):
    def specifications(self):
        return "slick tyres, optimal for dry and clean tracks"

class WetTyre(Tyre):
    def specifications(self):
        return "wet tyres, optimal for wet track conditions"

class GravelTyre(Tyre):
    def specifications(self):
        return "gravel tyres, designed for off-road and loose surfaces"

# Client code
def main():
    # Formula One Car with Slick Tyres
    slick_tyre = SlickTyre()
    f1_car = FormulaOneCar(slick_tyre)
    print(f1_car.description())

    # Formula One Car with Wet Tyres
    wet_tyre = WetTyre()
    f1_car_wet = FormulaOneCar(wet_tyre)
    print(f1_car_wet.description())

    # Rally Car with Gravel Tyres
    gravel_tyre = GravelTyre()
    rally_car = RallyCar(gravel_tyre)
    print(rally_car.description())

if __name__ == "__main__":
    main()

"""
Explanation:
1. **Vehicle (Abstraction Layer)**: This is the main abstraction. The Vehicle class takes a Tyre as a composition.
2. **FormulaOneCar and RallyCar (Refined Abstractions)**: These are concrete vehicle types that add more specific behavior to the general Vehicle abstraction.
3. **Tyre (Implementation Layer)**: Tyre represents the interface for tyres, with several different implementations like SlickTyre, WetTyre, and GravelTyre.
4. **Bridge Pattern**: This pattern helps to decouple the abstraction (Vehicle) from the implementation (Tyre). As a result, new types of Vehicles or Tyres can be added independently.
5. **Flexibility**: By using the bridge pattern, new tyre types can be easily integrated without altering the Vehicle class or its derived classes.
"""

```

