# Factory and Abstract Factory in Python

**Factory** and **Abstract Factory** are two patterns frequently applied when dealing with object creation. In the **Factory** design pattern, we encapsulate the object creation process in a method, allowing the code to rely on a common interface or abstract class rather than concrete implementations. **Abstract Factory** goes a step further: it allows for creating families of related objects without specifying their concrete classes.

![Factory Design Pattern Visual Representation](/Creational/Factory/res/factory.png)

The **Factory** pattern can be likened to Aristotle’s *potentiality* and *actuality*. The factory holds the potential to create an object, and it is through calling the factory method that the potential becomes actual. The **Abstract Factory**, however, can be seen as a reflection of **Plato's Theory of Forms**. The abstract factory represents the *idea* of a family of objects—an ideal or blueprint—while the concrete factories are instances of these forms in different contexts. Through abstraction, both patterns allow for higher-order thinking in code, moving away from specific instantiations towards generalized forms.

## The Factory Pattern

The Factory Pattern is a creational design pattern that simplifies object creation by using a centralized method, without needing to specify the exact class being instantiated. This pattern decouples the creation process from the code that uses the object, making it easier to manage and modify. By allowing the class to be determined at runtime based on certain conditions, the Factory Pattern provides flexibility, enabling developers to switch between different implementations without changing the client code. This makes the system more adaptable to future changes, promoting maintainability and scalability.

```python
from abc import ABC, abstractmethod

# Engine Interface - The abstract product
class Engine(ABC):
    @abstractmethod
    def assemble(self) -> str:
        pass

# Specific engines - Concrete Products
class Formula1Engine(Engine):
    def assemble(self) -> str:
        return "Assembling a high-performance Formula 1 engine!"

class RallyEngine(Engine):
    def assemble(self) -> str:
        return "Assembling a rugged Rally engine built for endurance!"

# Engine Factory
class EngineFactory:
    @staticmethod
    def create_engine(motorsport: str) -> Engine:
        if motorsport == "Formula 1":
            return Formula1Engine()
        elif motorsport == "Rally":
            return RallyEngine()
        else:
            raise ValueError(f"Unknown motorsport type: {motorsport}")

# Test Factory behavior
if __name__ == "__main__":

    # The client code doesn't need to know which 
    # specific engine class it is working with.
    first_engine = EngineFactory.create_engine("Formula 1")
    print(first_engine.assemble())

    second_engine = EngineFactory.create_engine("Rally")
    print(second_engine.assemble())                                                                           
```

## The Abstract Factory Pattern

The Abstract Factory Pattern extends the Factory Pattern by handling the creation of entire families of related products, rather than just a single product type. Its purpose is to provide an interface for generating groups of related objects without specifying their exact classes.

In essence, the Abstract Factory defines an interface with multiple methods, each responsible for creating a different type of product, while concrete factories implement these methods to produce cohesive sets of related products. This pattern is particularly useful when you have multiple families of products that must work together and want to ensure consistent creation across them. By centralizing the creation process for these related objects, the Abstract Factory ensures that products are compatible, promotes clean and organized design, and offers greater flexibility and maintainability in systems where different product families must be used together or swapped interchangeably.


```python
from abc import ABC, abstractmethod

# Engine Interface (Product)
class Engine(ABC):
    @abstractmethod
    def assemble(self) -> str:
        pass

# Chassis Interface (Product)
class Chassis(ABC):
    @abstractmethod
    def build(self) -> str:
        pass

# Aerodynamics Interface (Product)
class Aerodynamics(ABC):
    @abstractmethod
    def design(self) -> str:
        pass

# Concrete Products: Formula 1
class Formula1Engine(Engine):
    def assemble(self) -> str:
        return "Assembling a high-performance Formula 1 engine!"

class Formula1Chassis(Chassis):
    def build(self) -> str:
        return "Building a lightweight Formula 1 chassis."

class Formula1Aerodynamics(Aerodynamics):
    def design(self) -> str:
        return "Designing advanced aerodynamics for Formula 1."

# Concrete Products: Rally
class RallyEngine(Engine):
    def assemble(self) -> str:
        return "Assembling a rugged Rally engine built for endurance!"

class RallyChassis(Chassis):
    def build(self) -> str:
        return "Building a durable Rally chassis."

class RallyAerodynamics(Aerodynamics):
    def design(self) -> str:
        return "Designing aerodynamics optimized for Rally."

# Abstract Factory
class CarFactory(ABC):
    @abstractmethod
    def create_engine(self) -> Engine:
        pass

    @abstractmethod
    def create_chassis(self) -> Chassis:
        pass

    @abstractmethod
    def create_aerodynamics(self) -> Aerodynamics:
        pass

# Concrete Factories
class Formula1Factory(CarFactory):
    def create_engine(self) -> Engine:
        return Formula1Engine()

    def create_chassis(self) -> Chassis:
        return Formula1Chassis()

    def create_aerodynamics(self) -> Aerodynamics:
        return Formula1Aerodynamics()

class RallyFactory(CarFactory):
    def create_engine(self) -> Engine:
        return RallyEngine()

    def create_chassis(self) -> Chassis:
        return RallyChassis()

    def create_aerodynamics(self) -> Aerodynamics:
        return RallyAerodynamics()

# Client Code
def assemble_car(factory: CarFactory):
    engine = factory.create_engine()
    chassis = factory.create_chassis()
    aerodynamics = factory.create_aerodynamics()

    print(engine.assemble())
    print(chassis.build())
    print(aerodynamics.design())

# Test Abstract Factory behaviour
if __name__ == "__main__":
    print("Assembling a Formula 1 car:")
    f1_factory = Formula1Factory()
    assemble_car(f1_factory)

    print("\nAssembling a Rally car:")
    rally_factory = RallyFactory()
    assemble_car(rally_factory)
```

Both patterns abstract away the concrete instantiation of objects, the Factory pattern focuses on the creation of one product at a time, while the Abstract Factory manages the creation of entire families of related products.
