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
