from abc import ABC, abstractmethod
from typing import Dict


class Context:
    """
    Stores external information for variable resolution.
    This can include variable bindings for more complex cases.
    """
    def __init__(self):
        self.variables: Dict[str, int] = {}

    def set_variable(self, name: str, value: int) -> None:
        self.variables[name] = value

    def get_variable(self, name: str) -> int:
        return self.variables.get(name, 0)


class Expression(ABC):
    """
    Abstract base class for all expressions.
    Defines the interface for the interpret method.
    """
    @abstractmethod
    def interpret(self, context: Context) -> int:
        pass


class Number(Expression):
    """
    Terminal expression for numeric literals.
    Represents a single number.
    """
    def __init__(self, value: int) -> None:
        self.value = value

    def interpret(self, context: Context) -> int:
        return self.value


class Add(Expression):
    """
    Non-terminal expression for addition.
    Represents an operation that adds two sub-expressions.
    """
    def __init__(self, left: Expression, right: Expression) -> None:
        self.left = left
        self.right = right

    def interpret(self, context: Context) -> int:
        return self.left.interpret(context) + self.right.interpret(context)

# Example Usage
if __name__ == "__main__":
    # Construct the expression (3 + 5)
    context = Context()
    expression = Add(Add(Number(3), Number(5)), Number(2))
    print("Result:", expression.interpret(context))  # Output: 10