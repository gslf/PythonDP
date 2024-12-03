# The Object Pool design pattern

The Object Pool Pattern is a **creational** design pattern that manages a pool of reusable objects. It is particularly effective in scenarios where *the cost of object creation* is high and a limited number of instances is desired. The pattern aims to minimize resource overhead by reusing objects rather than instantiating them repeatedly. This is commonly seen in managing database connections, thread pools, or large datasets that are computationally expensive to create.

The Object Pool Pattern represents an efficient and deliberate economy of reuse. Much like ecological systems that thrive on reuse and optimization, software engineering can often benefit from carefully managing finite resources. This pattern is an embodiment of a resource-conscious mindset: rather than discarding an object after its purpose has been served, it is retained, refreshed, and put back into service.

![Object Pool Pattern Visual Representation](/ObjectPool/res/object_pool_visualization.png)

Imagine an Object Pool as a library. Instead of each person buying a copy of every book they need, people come to the library and borrow books for a period. When they are done, they return them to the library, making the books available for others to use. In the same way, the Object Pool holds a collection of reusable objects that are temporarily "borrowed" to perform specific tasks, and once completed, they are "returned" to the pool for future use.

## Implementation
This is an implementation of the Object Pool pattern:

```python
import queue
import time

# The Reusable object managed by the Object Pool
class Reusable:
    def __init__(self):
        # Simulate an initialization delay
        time.sleep(1)
        self.created_at = time.time()

    def do_work(self):
        print(f"Object created at {self.created_at} is doing work.")

# Simplified Object Pool class
class ObjectPool:
    def __init__(self, size=5):
        self.pool = queue.Queue(size)
        for _ in range(size):
            self.pool.put(Reusable())

    def acquire(self):
        # Acquire a reusable object from the pool, creating a new one if empty
        if self.pool.empty():
            print("Pool is empty, creating a new reusable object.")
            return Reusable()
        print("Acquired reusable object from pool.")
        return self.pool.get()

    def release(self, reusable):
        # Release the reusable object back to the pool if there is space
        if self.pool.full():
            print("Pool is full, discarding reusable object.")
        else:
            self.pool.put(reusable)
            print("Returned reusable object back to pool.")

# Example usage
def main():
    pool = ObjectPool(size=3)

    reusable1 = pool.acquire()
    reusable1.do_work()

    reusable2 = pool.acquire()
    reusable2.do_work()

    pool.release(reusable1)

    reusable3 = pool.acquire()
    reusable3.do_work()

    reusable4 = pool.acquire()
    reusable4.do_work()

if __name__ == "__main__":
    main()


```


In practice, an Object Pool is akin to a resource manager, maintaining a balance between the limited availability of resources and the potential high demand for them. Objects are created ahead of time, stored, and then made available for consumers. If all objects are in use, subsequent requests are either queued until one is released or a new instance is created as needed. In this way, object pools help alleviate performance bottlenecks and improve application efficiency.