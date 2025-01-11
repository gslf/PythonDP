# Strategy Design Pattern in Python
The Strategy design pattern is a behavioral pattern that enables selecting an algorithm's implementation at runtime. It represents a family of algorithms, encapsulates each one, and makes them interchangeable within that family. This pattern lets the algorithm vary independently from clients that use it.

The main philosophy behind the Strategy pattern is the principle "prefer composition over inheritance". Instead of building a monolithic class with multiple conditional statements to handle different algorithms, we separate each algorithm into its own class. This approach promotes code maintainability, reusability, and flexibility while reducing complexity.

The Strategy pattern consists of three main components:

- **Context:** Maintains a reference to a Strategy object and may define an interface that lets Strategy access its data
- **Strategy:** Declares an interface common to all supported algorithms
- **Concrete Strategies:** Implement different algorithms while following the Strategy interface

![Strategy Pattern Representation](/Behavioral/Strategy/res/strategy_visualization.png)

This pattern is similar to the State pattern, the key distinction lies in their intent: Strategy is about providing different ways to do the same thing, while State is about organizing state-dependent code where an object behaves differently based on its internal state.

A practical way to remember the difference is that in the Strategy pattern, the client typically decides which strategy to use and explicitly sets it, while in the State pattern, the states themselves manage transitions between each other based on the object's internal condition. Strategy is about "how" something is done, State is about "what" can be done at a particular moment.

## Implementation
Let's consider a real-world example: a payment processing system for an e-commerce platform. In this scenario, customers can choose different payment methods (PayPal, credit card, bank transfer) at checkout. Each payment method has its own processing logic, but they all need to handle the payment transaction.

Without the Strategy pattern, we might write a large and ugly PaymentProcessor class with multiple if-else statements to handle different payment methods. Instead, we can implement each payment method as a separate strategy, making our system more flexible and maintainable.

```python
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Protocol, Optional
from decimal import Decimal

# Payment details data structure
@dataclass
class PaymentDetails:
    amount: Decimal
    currency: str
    description: str

# Strategy interface
class PaymentStrategy(Protocol):
    def process_payment(self, payment: PaymentDetails) -> bool:
        """Process the payment and return whether it was successful"""
        ...

# Concrete strategies
class PayPalStrategy:
    def __init__(self, email: str, password: str):
        self.email = email
        self.password = password
    
    def process_payment(self, payment: PaymentDetails) -> bool:
        # In a real implementation, this would interact with PayPal's API
        print(f"Processing PayPal payment of {payment.amount} {payment.currency}")
        print(f"Using email: {self.email}")
        return True

class CreditCardStrategy:
    def __init__(self, card_number: str, expiry: str, cvv: str):
        self.card_number = card_number
        self.expiry = expiry
        self.cvv = cvv
    
    def process_payment(self, payment: PaymentDetails) -> bool:
        # In a real implementation, this would interact with a payment gateway
        print(f"Processing Credit Card payment of {payment.amount} {payment.currency}")
        print(f"Using card: ****{self.card_number[-4:]}")
        return True

class BankTransferStrategy:
    def __init__(self, iban: str, swift: str):
        self.iban = iban
        self.swift = swift
    
    def process_payment(self, payment: PaymentDetails) -> bool:
        # In a real implementation, this would interact with banking APIs
        print(f"Processing Bank Transfer of {payment.amount} {payment.currency}")
        print(f"Using IBAN: {self.iban}")
        return True

# Context
class PaymentProcessor:
    def __init__(self, strategy: Optional[PaymentStrategy] = None):
        self._strategy = strategy
    
    def set_payment_strategy(self, strategy: PaymentStrategy) -> None:
        self._strategy = strategy
    
    def process_payment(self, payment: PaymentDetails) -> bool:
        if self._strategy is None:
            raise ValueError("Payment strategy not set")
        return self._strategy.process_payment(payment)

# USAGE EXAMPLE

# Create payment details
payment = PaymentDetails(
    amount=Decimal("100.00"),
    currency="USD",
    description="Premium subscription"
)

# Create payment processor
processor = PaymentProcessor()

# Process payment using PayPal
paypal = PayPalStrategy("user@example.com", "password123")
processor.set_payment_strategy(paypal)
processor.process_payment(payment)

# Process payment using Credit Card
credit_card = CreditCardStrategy("1234567890123456", "12/25", "123")
processor.set_payment_strategy(credit_card)
processor.process_payment(payment)

# Process payment using Bank Transfer
bank_transfer = BankTransferStrategy("DE89370400440532013000", "DEUTDEFF")
processor.set_payment_strategy(bank_transfer)
processor.process_payment(payment)
```