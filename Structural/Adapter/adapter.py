class OldPaymentGateway:
    def process_payment(self, amount):
        return f"Payment of ${amount} processed through OldPaymentGateway."

class NewPaymentGateway:
    def make_transaction(self, amount):
        return f"Transaction of ${amount} completed using NewPaymentGateway."

# The Adapter
class PaymentAdapter:
    def __init__(self, payment_system):
        self.payment_system = payment_system

    def process_payment(self, amount):
        # Dynamically adapt the method based on the object being wrapped
        if hasattr(self.payment_system, 'process_payment'):
            return self.payment_system.process_payment(amount)
        elif hasattr(self.payment_system, 'make_transaction'):
            return self.payment_system.make_transaction(amount)
        else:
            raise NotImplementedError("This payment method is not supported by the adapter.")

# Usage Example
def main():
    old_gateway = OldPaymentGateway()
    new_gateway = NewPaymentGateway()

    # Adapting the old payment system
    adapter_old = PaymentAdapter(old_gateway)
    print(adapter_old.process_payment(100))

    # Adapting the new payment system
    adapter_new = PaymentAdapter(new_gateway)
    print(adapter_new.process_payment(200))

if __name__ == "__main__":
    main()