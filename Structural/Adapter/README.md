# The Adapter Patter in Python

The Adapter Design Pattern is a structural pattern that acts as a bridge between incompatible interfaces, making classes that otherwise couldn't work together, collaborate seamlessly. In Python, the Adapter Pattern is particularly effective due to the language's inherent flexibility and dynamic features. 

Imagine you're building a system that has to integrate with different third-party libraries, each with their own slightly different way of interacting with the same data. One library might be expecting a method named fetch(), while another wants retrieve(). Changing these libraries directly could be a maintenance nightmare, especially if you don't own the code. Enter the Adapter Pattern—an elegant solution that standardizes these interfaces without altering the underlying code.

![Adapter Pattern Visual Representation](/Adapter/res/adapter_visualization.png)

The Adapter doesn’t force changes upon existing objects; it allows them to coexist through translation. You can think of an adapter as a plug converter. Imagine you're traveling with a laptop that has a European plug, but you arrive in the United States where the sockets are different. The adapter bridges the gap, allowing your device to function without needing to change the wiring inside the socket or your plug.

## Implementation

This is an example implementation of the Adapter Pattern in Python.

```python
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
```

