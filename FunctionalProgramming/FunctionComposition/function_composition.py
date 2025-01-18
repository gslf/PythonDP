from typing import Callable
from functools import reduce
from decimal import Decimal

def compose(*functions: Callable) -> Callable:
    """
    Creates a new function that chains the given functions from right to left.
    """
    return reduce(lambda f, g: lambda x: f(g(x)), functions)

def apply_discount(price: Decimal, discount_percent: int = 10) -> Decimal:
    """
    Applies a percentage discount to the price
    Example: $100 with 10% discount becomes $90
    """
    discount = price * (Decimal(discount_percent) / Decimal(100))
    return price - discount

def add_tax(price: Decimal, tax_rate: int = 20) -> Decimal:
    """
    Adds tax to the price
    Example: $90 with 20% tax becomes $108
    """
    tax = price * (Decimal(tax_rate) / Decimal(100))
    return price + tax

def format_price(price: Decimal) -> str:
    """
    Formats price for display
    Example: 108.00 becomes '$108.00'
    """
    return f"${price:.2f}"

# Compose all functions into a single processing pipeline
calculate_final_price = compose(
    format_price,
    lambda price: add_tax(price, 20),
    lambda price: apply_discount(price, 10)
)

# Usage example
base_price = Decimal('100.00')
final_price = calculate_final_price(base_price)
print(final_price) # $108.00