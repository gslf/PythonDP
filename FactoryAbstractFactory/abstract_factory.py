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
