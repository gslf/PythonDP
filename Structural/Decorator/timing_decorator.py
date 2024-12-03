import functools
import time
from typing import Callable

def timing_decorator(func: Callable) -> Callable:
    """
    A decorator that prints the time a function takes to execute.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        print(f"Function {func.__name__!r} executed in {end_time - start_time:.4f} seconds.")
        return result
    return wrapper

@timing_decorator
def process_data(data: list) -> list:
    """
    Function to simulate processing some data.
    """
    # Simulating a time-consuming operation by processing a huge list
    result = [item * 2 for item in data]
    return result

if __name__ == "__main__":
    huge_list = list(range(10**7))
    result = process_data(huge_list)
    print("First 10 Processed :", result[:10])