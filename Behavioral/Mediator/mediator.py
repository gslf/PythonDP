from dataclasses import dataclass
from typing import Dict
from enum import Enum
import uuid

# Enums for aircraft status
class AircraftStatus(Enum):
    WAITING = "waiting"
    CLEARED_FOR_TAKEOFF = "cleared_for_takeoff"
    TAKING_OFF = "taking_off"
    AIRBORNE = "airborne"
    APPROACHING = "approaching"
    LANDED = "landed"

# Base class for aircraft (colleagues)
@dataclass
class Aircraft:
    id: str
    name: str
    status: AircraftStatus
    mediator: 'AirTrafficControl'
    
    def request_takeoff(self) -> None:
        self.mediator.notify(self, "request_takeoff")
    
    def request_landing(self) -> None:
        self.mediator.notify(self, "request_landing")
        
    def update_status(self, new_status: AircraftStatus) -> None:
        self.status = new_status
        print(f"Aircraft {self.name} status updated to: {new_status.value}")

# Mediator
class AirTrafficControl:
    def __init__(self) -> None:
        self.aircraft: Dict[str, Aircraft] = {}
        self.runway_occupied: bool = False
    
    def register_aircraft(self, aircraft: Aircraft) -> None:
        self.aircraft[aircraft.id] = aircraft
        print(f"Aircraft {aircraft.name} registered with control tower")
    
    def notify(self, aircraft: Aircraft, event: str) -> None:
        if event == "request_takeoff":
            self._handle_takeoff_request(aircraft)
        elif event == "request_landing":
            self._handle_landing_request(aircraft)
    
    def _handle_takeoff_request(self, aircraft: Aircraft) -> None:
        if not self.runway_occupied:
            print(f"Control tower: Clearing {aircraft.name} for takeoff")
            self.runway_occupied = True
            aircraft.update_status(AircraftStatus.CLEARED_FOR_TAKEOFF)
            # Simulate takeoff sequence
            aircraft.update_status(AircraftStatus.TAKING_OFF)
            aircraft.update_status(AircraftStatus.AIRBORNE)
            self.runway_occupied = False
        else:
            print(f"Control tower: {aircraft.name} must wait, runway occupied")
            aircraft.update_status(AircraftStatus.WAITING)
    
    def _handle_landing_request(self, aircraft: Aircraft) -> None:
        if not self.runway_occupied:
            print(f"Control tower: Clearing {aircraft.name} for landing")
            self.runway_occupied = True
            aircraft.update_status(AircraftStatus.APPROACHING)
            aircraft.update_status(AircraftStatus.LANDED)
            self.runway_occupied = False
        else:
            print(f"Control tower: {aircraft.name} must hold, runway occupied")
            aircraft.update_status(AircraftStatus.WAITING)

# Example usage

# Create the mediator (control tower)
control_tower = AirTrafficControl()

# Create aircraft
flight1 = Aircraft(str(uuid.uuid4()), "Flight AA123", AircraftStatus.WAITING, control_tower)
flight2 = Aircraft(str(uuid.uuid4()), "Flight BA456", AircraftStatus.AIRBORNE, control_tower)

# Register aircraft with control tower
control_tower.register_aircraft(flight1)
control_tower.register_aircraft(flight2)

# Simulate interactions
flight1.request_takeoff()  # First aircraft requests takeoff
flight2.request_landing()  # Second aircraft requests landing