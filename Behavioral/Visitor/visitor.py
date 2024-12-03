from abc import ABC, abstractmethod

# Visitor Interface
class CarPartVisitor(ABC):
    """
    The Visitor interface declares a set of visiting methods for each type of
    concrete element in the object structure.
    """
    @abstractmethod
    def visit_engine(self, engine: 'Engine') -> None:
        pass

# Concrete Visitor
class MaintenanceVisitor(CarPartVisitor):
    """
    Concrete Visitors implement several versions of the same algorithm, which can
    work with all concrete element classes.
    """
    def visit_engine(self, engine):
        print(f"Performing maintenance on the engine: {engine.check_engine()}")

# Element Interface
class CarPart(ABC):
    """
    The Element interface declares an `accept` method that takes the base visitor interface.
    """
    @abstractmethod
    def accept(self, visitor):
        pass

# Concrete Element: Engine
class Engine(CarPart):
    """
    Concrete Elements provide implementations of the `accept` method that calls
    the visitor's method corresponding to the element's class.
    """
    def accept(self, visitor):
        # The visitor's visit_engine method is called with this engine instance
        visitor.visit_engine(self)

    def check_engine(self):
        # Specific functionality of the Engine element
        return "Engine is running smoothly."




# Client Code
if __name__ == "__main__":
    # Create a car part
    race_engine = Engine()
    # Perform maintenance by accepting the visitor
    race_engine.accept(MaintenanceVisitor())
