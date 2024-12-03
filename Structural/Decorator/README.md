# The Decorator Pattern in Python
The Decorator Pattern allows behavior to be added to an object dynamically. In Python, decorators are often **functions that wrap other functions**, enabling the extension of their behavior without explicitly modifying their structure. This makes them an essential tool for writing modular, reusable, and DRY (Don't Repeat Yourself) code.

You can imagine the Decorator Pattern as **layers of clothing**. You have a basic shirt, and then you add a jacket, a hat, and a scarf. Each new layer adds functionality (like warmth or style) but doesn’t change the core shirt.

![Decorator Pattern Visual Representation](/Decorator/res/decorator_visualization.png)

## Implementation
This is a basic implementation of a Decorator in Python:

```python
def simple_decorator(func):
    def wrapper():
        print("Something is happening before the function is called.")
        func()
        print("Something is happening after the function is called.")
    return wrapper

@simple_decorator
def say_hello():
    print("Hello!")

say_hello()
```

This basic example helps clarify the mechanics of a decorator, but let’s take it a step further by implementing one with practical utility. Here’s a **timing decorator** designed to measure execution time, offering insights directly applicable to performance tuning and optimization.

```python
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
```

The decorated function is a metaphor for a system that learns and adapts, gaining new behaviors over time without losing its core identity. It’s about protecting the core of what something is, while building additional attributes around it, much like adding skills to an individual’s repertoire without altering who they are fundamentally.