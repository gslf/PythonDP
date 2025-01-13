from dataclasses import dataclass
from abc import ABC, abstractmethod

# Base shape class
class Shape(ABC):
    def __init__(self, x: float, y: float):
        self.position = (x, y)
        self.rotation = 0.0

    @abstractmethod
    def render(self) -> None:
        pass

# Concrete shapes
@dataclass
class Circle(Shape):
    radius: float

    def __init__(self, x: float, y: float, radius: float = 1.0):
        super().__init__(x, y)
        self.radius = radius

    def render(self) -> None:
        print(f"Drawing circle at {self.position} with radius {self.radius}")

@dataclass
class Rectangle(Shape):
    width: float
    height: float

    def __init__(self, x: float, y: float, width: float = 2.0, height: float = 1.0):
        super().__init__(x, y)
        self.width = width
        self.height = height

    def render(self) -> None:
        print(f"Drawing rectangle at {self.position} with dimensions {self.width}x{self.height}")

# The Servant class
class MovementServant:
    @staticmethod
    def move(shape: Shape, dx: float, dy: float) -> None:
        """Moves a shape by the specified delta coordinates"""
        x, y = shape.position
        shape.position = (x + dx, y + dy)

##############################
# Example Usage
# Create Shapes
circle = Circle(0, 0, radius=5.0) 
rectangle = Rectangle(10, 10, width=4.0, height=2.0)  

# Initial State
print("Initial State:")
circle.render()
rectangle.render()

# Movements
MovementServant.move(circle, 3, 4)  
MovementServant.move(rectangle, -5, 0)

# Final State
print("\nFinal State after movements:")
circle.render()
rectangle.render()