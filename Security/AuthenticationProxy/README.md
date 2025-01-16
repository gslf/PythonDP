# Authentication Proxy in python
The Authentication Proxy acts as a protective layer between clients and sensitive resources by introducing an intermediary proxy object that handles authentication and authorization before allowing access to the protected resource. 

By delegating authentication responsibilities to a dedicated proxy, the actual resource remains focused on its core functionality while security concerns are managed separately. This separation enhances maintainability and allows for security policy modifications without affecting the protected resource's implementation.

The pattern consists of three main components: 

- the Subject interface, 
- the Real Subject, 
- the Authentication Proxy. 

The Subject interface defines the common interface that both the proxy and real subject must implement. The Real Subject contains the actual business logic, while the Authentication Proxy wraps the real subject and handles security checks.

![Authentication proxy - Visual Representation](/Security/AuthenticationProxy/res/authentication_proxy.png)


## Implementation
Consider a banking system where customers access their account information through an API. The actual account data (Real Subject) should never be directly accessible. Instead, an Authentication Proxy verifies the customer's identity and permissions before allowing any operation.

When a customer requests their balance:

1. The request first hits the Authentication Proxy
2. The proxy validates the customer's credentials and session token
3. If authentication passes, the proxy checks if the customer has permission to view the requested account
4. Only then does the proxy forward the request to the actual Account Service
5. The Account Service returns the balance, which the proxy relays back to the customer

```python
from abc import ABC, abstractmethod
from typing import Dict, Optional
from dataclasses import dataclass

# Data structures
@dataclass
class User:
    username: str
    password: str

@dataclass
class BankAccount:
    account_id: str
    balance: float
    owner_username: str

# Exceptions
class AuthenticationError(Exception):
    """Raised when authentication fails."""
    pass

class AuthorizationError(Exception):
    """Raised when a user is not authorized to access a resource."""
    pass

# Subject interface
class BankAccountService(ABC):
    @abstractmethod
    def get_balance(self, account_id: str) -> float:
        pass

    @abstractmethod
    def get_account_owner(self, account_id: str) -> Optional[str]:
        pass

# Real Subject - The actual bank account service
class RealBankAccountService(BankAccountService):
    def __init__(self):
        self._accounts: Dict[str, BankAccount] = {
            "ACC001": BankAccount("ACC001", 1000.0, "alice"),
            "ACC002": BankAccount("ACC002", 2500.0, "bob")
        }

    def get_balance(self, account_id: str) -> float:
        account = self._accounts.get(account_id)
        if not account:
            raise ValueError(f"Account with ID {account_id} does not exist.")
        return account.balance

    def get_account_owner(self, account_id: str) -> Optional[str]:
        """Returns the owner of the account, or None if the account does not exist."""
        account = self._accounts.get(account_id)
        return account.owner_username if account else None

# Authentication Proxy
class AuthenticatedBankService():
    def __init__(self, real_service: BankAccountService):
        self._real_service = real_service
        self._users: Dict[str, User] = {
            "alice": User("alice", "pass123"),
            "bob": User("bob", "pass456"),
        }
        self._logged_in_user: Optional[str] = None  # Tracks the currently logged-in user

    def login(self, username: str, password: str) -> None:
        """Authenticate user."""
        user = self._users.get(username)
        if user and user.password == password:
            self._logged_in_user = username
        else:
            raise AuthenticationError("Invalid username or password.")

    def logout(self) -> None:
        """Log out the currently logged-in user."""
        self._logged_in_user = None

    def get_balance(self, account_id: str) -> float:
        """Get the balance of a bank account if the user is authenticated."""
        if not self._logged_in_user:
            raise AuthenticationError("User not logged in.")

        # Check if the logged-in user is the owner of the account
        owner = self._real_service.get_account_owner(account_id)
        if owner != self._logged_in_user:
            raise AuthorizationError("Access denied.")
        
        return self._real_service.get_balance(account_id)

# Example usage
if __name__ == "__main__":
    real_service = RealBankAccountService()
    auth_service = AuthenticatedBankService(real_service)

    try:
        # User login
        username = "alice"
        auth_service.login(username, "pass123")
        print(f"{username} logged in successfully.")

        # Access Alice's account
        balance = auth_service.get_balance("ACC001")
        print(f"{username}'s balance: ${balance}")

        # Attempt to access Bob's account (unauthorized)
        balance = auth_service.get_balance("ACC002")
        print(f"Bob's balance: ${balance}")
    except (AuthenticationError, AuthorizationError, ValueError) as e:
        print(f"Error: {e}")

    # Logout
    auth_service.logout()
    print("User logged out.")
```

