# Producer-Consumer - Concurrency in Python
The Producer-Consumer pattern represents a fundamental paradigm in concurrent programming where **producers** generate data and **consumers** process it, operating **independently** but sharing a common data buffer. This pattern effectively decouples data production from its consumption, enabling parallel processing and improved system efficiency.

In modern software systems, we often face scenarios where data **generation and processing occur at different rates**. Think of a web server receiving requests (producer) and worker threads processing them (consumers). Without proper synchronization, fast producers might overwhelm slow consumers, or processors might stay idle waiting for data.

The pattern consists of three main components:

- **Producer:** Creates and adds data to the shared buffer
- **Consumer:** Retrieves and processes data from the buffer
- **Shared Buffer:** Thread-safe queue with synchronization mechanisms

The **synchronization** ensures that producers wait when the buffer is full, consumers wait when the buffer is empty, and that buffer access is thread-safe.

![Producers - Consumer Visual Representation](/Concurrency/ProducerConsumer/res/producer_consumers_visualization.png)

## Implementation

Consider a modern Formula 1 car's telemetry system:

- **Multiple sensors** (producers) constantly collect data about the car: engine temperature, tire pressure, fuel consumption, speed, G-forces, etc.
- **Analysis units** (consumers) process this data to provide real-time insights to engineers
- The **telemetry buffer** (shared buffer) temporarily stores sensor readings

If the sensors collect data faster than it can be processed (buffer full), they must wait before adding new readings. If there's no data (buffer empty), analysis units wait for new readings. This system ensures no critical car performance data is lost or processed incorrectly, regardless of the speed of data collection or analysis.


```python
from queue import Queue
from threading import Thread, Event
from dataclasses import dataclass
from typing import  List
from abc import ABC
import time
import random

@dataclass
class TelemetryData:
    timestamp: float
    sensor_id: int
    data_type: str
    value: float
    unit: str

class Sensor(ABC):
    def __init__(self, sensor_id: int, name: str, unit: str, min_value: float, max_value: float):
        self.sensor_id = sensor_id
        self.name = name
        self.unit = unit
        self.min_value = min_value
        self.max_value = max_value
    
    def read(self) -> TelemetryData:
        """Generate a sensor reading"""
        return TelemetryData(
            timestamp=time.time(),
            sensor_id=self.sensor_id,
            data_type=self.name,
            value=random.uniform(self.min_value, self.max_value),
            unit=self.unit
        )

class EngineTemperatureSensor(Sensor):
    def __init__(self, sensor_id: int):
        super().__init__(sensor_id, "ENGINE_TEMP", "°C", 80, 120)

class TirePressureSensor(Sensor):
    def __init__(self, sensor_id: int):
        super().__init__(sensor_id, "TIRE_PRESSURE", "bar", 1.8, 2.5)

class SpeedSensor(Sensor):
    def __init__(self, sensor_id: int):
        super().__init__(sensor_id, "SPEED", "km/h", 0, 350)

class GForceSensor(Sensor):
    def __init__(self, sensor_id: int):
        super().__init__(sensor_id, "G_FORCE", "G", 0, 6)

class FuelLevelSensor(Sensor):
    def __init__(self, sensor_id: int):
        super().__init__(sensor_id, "FUEL_LEVEL", "%", 0, 100)

class F1TelemetrySystem:
    def __init__(self, buffer_size: int = 100):
        self.telemetry_queue: Queue[TelemetryData] = Queue(maxsize=buffer_size)
        self.sensor_types = [
            EngineTemperatureSensor,
            TirePressureSensor,
            SpeedSensor,
            GForceSensor,
            FuelLevelSensor
        ]
        # Add shutdown event for coordinating thread termination
        self.shutdown_event = Event()
        # Keep track of all threads
        self.threads: List[Thread] = []
        
    def sensor_worker(self, sensor: Sensor) -> None:
        """Worker function that continuously reads from a sensor"""
        while not self.shutdown_event.is_set():
            try:
                # Get sensor reading
                reading = sensor.read()
                
                # Put the reading in the queue with timeout
                # This ensures we can exit even if queue is full
                self.telemetry_queue.put(reading, timeout=1)
                print(f"Sensor {reading.sensor_id} ({reading.data_type}): "
                      f"Recorded {reading.value:.2f} {reading.unit}")
                
                # Simulate sensor reading frequency
                # Use wait instead of sleep to respond to shutdown quickly
                if self.shutdown_event.wait(random.uniform(0.1, 0.5)):
                    break
                    
            except Queue.Full:
                continue  # If queue is full, try again
            except Exception as e:
                print(f"Error in sensor {sensor.sensor_id}: {e}")
                break

    def analyzer(self, analyzer_id: int) -> None:
        """Simulates a telemetry analyzer processing data"""
        thresholds = {
            "ENGINE_TEMP": (lambda x: x > 110, "High engine temperature"),
            "TIRE_PRESSURE": (lambda x: x < 1.9, "Low tire pressure"),
            "SPEED": (lambda x: x > 340, "Approaching top speed"),
            "G_FORCE": (lambda x: x > 5.5, "Extreme G-Force detected"),
            "FUEL_LEVEL": (lambda x: x < 15, "Low fuel warning")
        }

        while not self.shutdown_event.is_set():
            try:
                # Get a reading from the queue with timeout
                reading = self.telemetry_queue.get(timeout=1)
                
                print(f"Analyzer {analyzer_id} processing {reading.data_type}: "
                      f"{reading.value:.2f} {reading.unit}")
                
                # Use wait instead of sleep
                if self.shutdown_event.wait(random.uniform(0.2, 0.7)):
                    break
                
                if reading.data_type in thresholds:
                    check_func, warning_msg = thresholds[reading.data_type]
                    if check_func(reading.value):
                        print(f"WARNING: {warning_msg}: {reading.value:.2f} {reading.unit}")
                
                self.telemetry_queue.task_done()
                
            except Queue.Empty:
                continue  # If queue is empty, try again
            except Exception as e:
                print(f"Error in analyzer {analyzer_id}: {e}")
                break

    def start_telemetry(self, sensors_per_type: int = 1, num_analyzers: int = 3) -> None:
        """Starts the telemetry system with specified sensors and analyzers"""
        # Reset shutdown event and threads list
        self.shutdown_event.clear()
        self.threads.clear()

        # Create sensors and their threads
        for sensor_type in self.sensor_types:
            for i in range(sensors_per_type):
                sensor = sensor_type(len(self.threads))
                thread = Thread(
                    target=self.sensor_worker,
                    args=(sensor,),
                    daemon=True
                )
                self.threads.append(thread)

        # Create analyzer threads
        for i in range(num_analyzers):
            thread = Thread(
                target=self.analyzer,
                args=(i,),
                daemon=True
            )
            self.threads.append(thread)

        # Start all threads
        for thread in self.threads:
            thread.start()

        try:
            # Keep the main thread alive
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\nInitiating shutdown sequence...")
            self.shutdown()

    def shutdown(self) -> None:
        """Perform a clean shutdown of the telemetry system"""
        print("Stopping all sensors and analyzers...")
        # Signal all threads to stop
        self.shutdown_event.set()
        
        # Wait for all threads to finish with timeout
        for i, thread in enumerate(self.threads):
            thread.join(timeout=2)
            if thread.is_alive():
                print(f"Thread {i} didn't shutdown gracefully")
        
        # Clear the queue
        while not self.telemetry_queue.empty():
            try:
                self.telemetry_queue.get_nowait()
                self.telemetry_queue.task_done()
            except Queue.Empty:
                break
                
        print("Telemetry system shutdown complete")
    

###################################
# Usage example:
telemetry = F1TelemetrySystem()
telemetry.start_telemetry(sensors_per_type=1, num_analyzers=3)
```