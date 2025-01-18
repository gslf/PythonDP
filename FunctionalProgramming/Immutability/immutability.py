from typing import NamedTuple, Tuple
from decimal import Decimal

# Immutable data containers using NamedTuple
Setup = NamedTuple('Setup', [
    ('front_wing_angle', int),    # degrees
    ('rear_wing_angle', int),     # degrees  
    ('tire_pressure', Decimal),    # PSI
    ('brake_bias', int)           # percentage to front
])

def adjust_for_condition(setup: Setup, condition: int) -> Setup:
    """Pure function that returns a new setup based on track condition.
    
    Args:
        setup: Current car setup configuration
        condition: Track condition (1=dry, 2=wet)
        
    Returns:
        A new Setup instance with adjusted values for the given condition
    """
    if condition == 1:  # dry
        return Setup(
            front_wing_angle=setup.front_wing_angle - 2,
            rear_wing_angle=setup.rear_wing_angle - 3,
            tire_pressure=setup.tire_pressure - Decimal("2.0"),
            brake_bias=setup.brake_bias - 2
        )
    elif condition == 2:  # wet
        return Setup(
            front_wing_angle=setup.front_wing_angle + 2,
            rear_wing_angle=setup.rear_wing_angle + 3,
            tire_pressure=setup.tire_pressure + Decimal("2.0"),
            brake_bias=setup.brake_bias + 2
        )
    return setup

def print_setup(setup: Setup) -> None:
    """Pure function that prints the current setup configuration.
    
    Args:
        setup: Car setup configuration to display
    """
    print(f"Wings: f {setup.front_wing_angle}° - r {setup.rear_wing_angle}°")
    print(f"Tire Pressure: {setup.tire_pressure} PSI")
    print(f"Brake Bias: {setup.brake_bias}%")
    print("=============================================================")

# Usage example with immutability
initial_setup = Setup(
    front_wing_angle=24,
    rear_wing_angle=20,
    tire_pressure=Decimal("28.5"),
    brake_bias=58
)

# Setup history as immutable tuple
setup_history: Tuple[Setup, ...] = (initial_setup,)
print_setup(setup_history[-1])

# Create new history with new setup
new_setup = adjust_for_condition(setup_history[-1], 2)
setup_history = setup_history + (new_setup,)
print_setup(setup_history[-1])

# "Rollback" by creating new history without last element
setup_history = setup_history[:-1]
print_setup(setup_history[-1])