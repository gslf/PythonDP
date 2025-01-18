# Currying in Python
Function currying is a fundamental transformation technique in functional programming where a function that takes multiple arguments is converted into a sequence of functions, each taking a single argument. 

A curried function transforms **f(x, y, z)** into **f(x)(y)(z)**. Each function call returns a new function that accepts the next argument until all arguments are provided. The final function in the chain executes the actual computation with all collected arguments.

![Currying Visual Representation](/FunctionalProgramming/Currying/res/currying_visualization.png)

## Implementation
Consider a Formula 1 engineering team that needs to calculate a car's theoretical lap time based on:

- Base lap time (in optimal conditions)
- Track temperature effect
- Tire degradation factor

```python
from typing import Callable
from decimal import Decimal

def lap_time_calculator(base_lap_time: Decimal) -> Callable[[Decimal], Callable[[Decimal], Decimal]]:
    """
    Creates a curried lap time calculator function.
    
    Args:
        base_lap_time: The optimal lap time in seconds
                      (e.g., 80.5 for 1:20.500)
        
    Returns:
        A function that takes temperature impact and returns another function
        that takes tire degradation factor
    """
    
    def with_temperature(temp_impact: Decimal) -> Callable[[Decimal], Decimal]:
        """
        Applies temperature effect on lap time.
        Track temperature impact is expressed as a coefficient
        (e.g., 1.02 means 2% slower due to temperature)
        
        Args:
            temp_impact: Temperature coefficient
        """
        def with_tire_deg(tire_degradation: Decimal) -> Decimal:
            """
            Calculates final lap time considering temperature and tire wear.
            
            Args:
                tire_degradation: Tire wear factor
                (e.g., 1.05 means 5% slower due to tire wear)
            """
            temp_adjusted_time = base_lap_time * temp_impact
            final_lap_time = temp_adjusted_time * tire_degradation
            return round(final_lap_time, 3)
        
        return with_tire_deg
    
    return with_temperature

# Usage examples:
# Create a calculator for Silverstone with base lap time of 80.5 seconds
silverstone_calculator = lap_time_calculator(Decimal('80.500'))

# Create a specific calculator for hot conditions (2% slower)
hot_condition_calculator = silverstone_calculator(Decimal('1.02'))

# Calculate different scenarios
optimal_lap = hot_condition_calculator(Decimal('1.0'))  # New tires
worn_tires_lap = hot_condition_calculator(Decimal('1.05'))  # 5% degradation

print(f"Optimal hot lap: {optimal_lap:.3f}s")  # Outputs: Optimal hot lap: 82.110s
print(f"Worn tires lap: {worn_tires_lap:.3f}s")  # Outputs: Worn tires lap: 86.216s

# Create another calculator for different track conditions
cold_condition_calculator = silverstone_calculator(Decimal('1.01'))
cold_worn_tires = cold_condition_calculator(Decimal('1.05'))
print(f"Cold track, worn tires: {cold_worn_tires:.3f}s")  # Outputs: Cold track, worn tires: 85.414s
```

The currying in this code allows progressive configuration of the lap time calculator. Starting with the base lap time, the first function (lap_time_calculator) creates a specialized calculator for a specific track. The second function (with_temperature) adjusts for temperature impact, and the third function (with_tire_deg) calculates the final lap time considering tire degradation. This approach makes it practical to predefine intermediate calculators, such as hot_condition_calculator or cold_condition_calculator, which can then be reused for multiple scenarios. It simplifies the process of handling combinations of parameters, like adjusting for both temperature and tire wear incrementally, without redefining the entire calculation logic.