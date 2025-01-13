# Servant Design Pattern in Python
The Servant design pattern is a behavioral pattern that defines a class which provides common functionality to a group of classes without being part of those classes. Unlike traditional inheritance or composition patterns, the Servant acts as a utility provider that any compatible class can leverage, promoting code reusability and separation of concerns.

The core philosophy behind the Servant pattern stems from the **"favor composition over inheritance"** principle, but takes it a step further. Instead of embedding functionality directly into classes or creating deep inheritance hierarchies, the Servant pattern extracts common behaviors into standalone service providers.

**The Servant pattern consists of two main components:**

- The Servant class that provides the functionality (the service provider)
- The client classes that can utilize the Servant's services (the service consumers)

The key characteristic is that the Servant operates on the client classes from the outside, requiring only that they meet certain minimal requirements or interfaces to be serviced.

![Servant Pattern Visual Representation](/Behavioral/Servant/res/servant_visualization.png)

## Implementation
Consider a 2D game with different types of geometric shapes (circles, rectangles, triangles) that need to move around the screen. Each shape has its own properties and rendering logic, but they all need similar movement capabilities. Instead of implementing movement methods in each shape class or creating a complex inheritance hierarchy, we can create a MovementServant that handles all movement-related operations.

The MovementServant can provide functions like move, rotate, and bounce for any shape that has a position and rotation property. This way, shapes can focus on their core properties and rendering while delegating movement behavior to the servant.

```python
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
```