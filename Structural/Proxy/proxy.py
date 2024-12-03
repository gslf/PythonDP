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

