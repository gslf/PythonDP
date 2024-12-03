# Chain Responsibility Design Pattern

The Chain of Responsibility (CoR) is a behavioral design pattern that allows passing requests along a chain of handlers. Each handler decides either to process the request or to pass it to the next handler in the chain. The main goal is to achieve loose coupling by giving multiple objects a chance to handle the request without the sender knowing which object will ultimately deal with it.

This pattern is particularly useful when you have multiple scenarios for handling requests, and the specific scenario is determined at runtime. CoR promotes open-ended extension as new handlers can be added to the chain with minimal modifications to existing code, adhering to the Open/Closed Principle.

![Chain Responsibility - Visual Representation](/ChainResponsibility/res/chain_responsibility_visualization.png)

Think of the Chain of Responsibility as a series of interconnected nodes, each representing a potential handler for a request. Imagine a production line where a defective product is inspected at each stage; each station checks the product, and if that specific station can't fix the defect, it passes the product to the next station in the line.

Some of the typical use cases for Chain of Responsibility:
- **Logging mechanisms**, where different log levels (info, warning, error) are handled by different handlers.
- **Middleware** in web frameworks, where requests pass through several layers of checks or modifications.
- **Event handling**, where issues are escalated through a chain until resolved.

## Implementation

Now, let’s look at a simplified real-world implementation of the Chain of Responsibility pattern using Python. We'll use a motorsport example where different team members handle different issues with a race car.

```python
class Handler:
    """
    Base handler class for the chain of responsibility.
    """
    def __init__(self, successor=None):
        self.successor = successor

    def handle(self, issue):
        if self.successor:
            return self.successor.handle(issue)
        return f"Issue '{issue}' could not be resolved."

class Mechanic(Handler):
    """
    Handles mechanical issues.
    """
    def handle(self, issue):
        if issue == "mechanical":
            return "Mechanic: Fixed the mechanical issue."
        return super().handle(issue)

class Electrician(Handler):
    """
    Handles electrical issues.
    """
    def handle(self, issue):
        if issue == "electrical":
            return "Electrician: Fixed the electrical issue."
        return super().handle(issue)

class PitCrew(Handler):
    """
    Handles pit stop related issues (e.g., tire change).
    """
    def handle(self, issue):
        if issue == "pit stop":
            return "PitCrew: Handled the pit stop."
        return super().handle(issue)


if __name__ == "__main__":
    # Setting up the chain of responsibility
    pit_crew = PitCrew()
    electrician = Electrician(successor=pit_crew)
    mechanic = Mechanic(successor=electrician)

    # Handling different issues
    issues = ["mechanical", "electrical", "pit stop", "aero"]
    
    for issue in issues:
        result = mechanic.handle(issue)
        print(f"{issue.capitalize()} Issue: {result}")
```