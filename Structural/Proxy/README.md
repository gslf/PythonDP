# The Proxy Design Pattern

The Proxy Design Pattern serves as an intermediary for another object, controlling or enhancing the access to that object. Essentially, it creates an extra layer of abstraction, enabling additional behavior, such as lazy instantiation, logging, access control, or even caching, without changing the original object’s structure or behavior.

Imagine you have a high-performance image processing class that is extremely resource-intensive to initialize. Using a proxy, you can defer the costly instantiation until absolutely needed. Additionally, proxies can be used to add a layer of security by validating the credentials before giving access to the real subject.

![Proxy Pattern Visual Representation](/Proxy/res/proxy_visualization.png)



# How it work

There are several variations of proxies, each designed to fulfill specific purposes:

- **Virtual Proxy:** Manages the instantiation of expensive resources.
- **Protection Proxy:** Controls access to the object by adding authentication or authorization logic.
- **Remote Proxy:** Acts as a local representative for an object that resides in a different address space.
- **Smart Proxy:** Adds additional behavior when the object is accessed, such as reference counting or logging.

## Implementation

This example will demonstrate use case where a Protection Proxy is used to control access to a sensitive resource, such as a bank account. The example provided is intentionally simplified—a static passkey like "1234" is not a secure solution. However, it effectively illustrates the core concept of this design pattern for demonstration purposes.

```python
class BankAccount():
    # A class representing a basic bank account with balance management.

    def __init__(self, balance):
        self._balance = balance

    def withdraw(self, amount):
        # Withdraw a specified amount from the bank account if funds are sufficient.
        if amount > self._balance:
            print(f"BankAccount: Insufficient funds. Available balance: ${self._balance}")
        else:
            self._balance -= amount
            print(f"BankAccount: Withdrawal of ${amount} successful. Remaining balance: ${self._balance}")

class ProtectionProxy(BankAccount):
    # The proxy class for protecting access to a bank account.

    def __init__(self, real_account: BankAccount):
        self._real_account = real_account
        self._authenticated = False

    def authenticate(self, pin):
        # Example of authentication logic
        if pin == "1234":
            self._authenticated = True
            print("ProtectionProxy: Authentication successful.")
        else:
            print("ProtectionProxy: Authentication failed.")

    def withdraw(self, amount):
        if self._authenticated:
            print("ProtectionProxy: Access granted. Forwarding the request to the real bank account.")
            self._real_account.withdraw(amount)
        else:
            print("ProtectionProxy: Access denied. Please authenticate first.")

if __name__ == "__main__":
    real_account = BankAccount(500)
    proxy = ProtectionProxy(real_account)
    
    # Attempting to withdraw without authentication
    print("\nClient attempting to withdraw without authentication:")
    proxy.withdraw(10)

    # Authenticating and then withdrawing
    print("\nPin required, insert pin (1234):")
    proxy.authenticate(input())
    proxy.withdraw(10)

```