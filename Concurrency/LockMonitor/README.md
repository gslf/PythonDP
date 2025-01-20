# Lock Monitor - Concurrency in Python
The Lock/Monitor pattern is a concurrency control mechanism commonly used to manage access to shared resources, ensuring that only one thread can access a resource at a time while allowing others to wait until it becomes available. This pattern helps prevent race conditions, deadlocks, and resource contention.

When a thread wants to access a shared resource, it must first acquire the lock associated with the monitor. If the lock is available, the thread can proceed to access the resource. If the lock is already held by another thread, the requesting thread will block and wait until the lock is released.

Once the thread has finished its operation on the resource, it releases the lock, allowing other waiting threads to acquire it. Condition variables can be used to signal one or more waiting threads when the resource becomes available.

![Lock/Monitor Visual Representation](/Concurrency/LockMonitor/res/lock_visualization.png)

## Implementation
Consider a banking system where multiple threads represent different bank customers trying to withdraw money from a shared bank account. The account has a limited balance, and we need to ensure that withdrawals do not exceed the available funds.

The scenario is this. Two customers attempt to withdraw money simultaneously. If both customers check the balance at the same time, they may see a sufficient balance and proceed with their withdrawals, potentially resulting in an overdraft.

```python
import threading
import time

class BankAccount:
    def __init__(self, initial_balance):
        self.balance = initial_balance
        self.lock = threading.Lock()  # Lock to control access to the balance

    def withdraw(self, amount):
        with self.lock:  # Acquire the lock
            if amount <= self.balance:
                print(f"Withdrawing {amount}. Current balance: {self.balance}")
                time.sleep(1)  # Simulate time taken to process the withdrawal
                self.balance -= amount
                print(f"Withdrawn {amount}. New balance: {self.balance}")
            else:
                print(f"Withdrawal of {amount} denied. Insufficient funds. Current balance: {self.balance}")

def customer_withdraw(account, amount):
    account.withdraw(amount)


#####################
# Example Usage

account = BankAccount(100)  # Initial balance

# Creating threads for customers
customer1 = threading.Thread(target=customer_withdraw, args=(account, 70))
customer2 = threading.Thread(target=customer_withdraw, args=(account, 80))

customer1.start()
customer2.start()

customer1.join()
customer2.join()

print(f"Final balance: {account.balance}")
```

**Explanation of the Code**

- **BankAccount Class:** This class represents a bank account with a balance and a locking mechanism. The withdraw method is responsible for managing withdrawals.
- **Lock Usage:** The with self.lock statement ensures that the lock is acquired before accessing the balance and automatically released after the block is exited.
- **Customer Withdraw Function:** This function simulates a customer trying to withdraw a specified amount.
Thread Creation: Two threads are created to simulate concurrent withdrawal attempts.