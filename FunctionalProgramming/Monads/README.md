# Monads in Python
The Function Monad pattern is used in Functional Programming to create a consistent way to chain operations while keeping the code linear and maintainable. 

A monad is a type that wraps another type and implements two fundamental operations::

- A **unit** function (often called "return") that wraps a value in the monad
- A **bind** operation (often called "map" or "flatMap") that chains operations

A monad must satisfy three mathematical laws:

- **Left identity:** unit(x).bind(f) ≡ f(x)
- **Right identity:** m.bind(unit) ≡ m
- **Associativity:** m.bind(f).bind(g) ≡ m.bind(x => f(x).bind(g))

![Monads Visual Representation](/FunctionalProgramming/Monads/res/monads_visualization.png)


## Implementation
Let's consider a practical example: Processing a payment. We need to:

- Validate the payment amount
- Check if there are sufficient funds
- Apply transaction fees
- Format the final receipt

Each step could potentially fail (invalid amount, insufficient funds), and we want to handle these cases gracefully. The Function Monad pattern helps us chain these operations in a clean way.

```python
from typing import Optional, Callable, TypeAlias, Tuple

# Type aliases for clarity
Result: TypeAlias = Tuple[Optional[float], Optional[str]]

def success(value: float) -> Result:
    """Create a successful result"""
    return (value, None)

def fail(error: str) -> Result:
    """Create a failed result"""
    return (None, error)

def then(result: Result, func: Callable[[float], Result]) -> Result:
    """Chain operations together"""
    value, error = result
    if error:
        return result
    if value is None:
        return fail("No value present")
    return func(value)

# Payment processing functions
def validate_amount(amount: float) -> Result:
    """Check if amount is valid"""
    if amount <= 0:
        return fail("Amount must be positive")
    return success(amount)

def check_balance(amount: float) -> Result:
    """Check if there are sufficient funds"""
    available_balance = 1000  # Simulated balance
    if amount > available_balance:
        return fail("Insufficient funds")
    return success(amount)

def apply_fee(amount: float) -> Result:
    """Apply 2% transaction fee"""
    return success(amount * 1.02)  # Add 2% fee

def format_receipt(amount: float) -> Result:
    """Format the final amount"""
    return success(round(amount, 2))



def process_payment(amount: float) -> Result:
    """Process payment chaining using reduce"""
    operations = [
        validate_amount,
        check_balance,
        apply_fee,
        format_receipt
    ]
    
    result = success(amount)
    for operation in operations:
        result = then(result, operation)
    
    return result


#############################
# Example Usage

# Successful payment
success_case = process_payment(100)
print(f"Success case: {success_case}")  # (102.0, None)

# Invalid amount
invalid_case = process_payment(-50)
print(f"Invalid amount: {invalid_case}")  # (None, 'Amount must be positive')

# Insufficient funds
insufficient_case = process_payment(2000)
print(f"Insufficient funds: {insufficient_case}")  # (None, 'Insufficient funds')


```