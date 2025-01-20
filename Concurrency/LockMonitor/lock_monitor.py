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