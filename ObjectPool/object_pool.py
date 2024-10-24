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
