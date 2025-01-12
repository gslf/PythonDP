from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List
from enum import Enum, auto

class AnalysisState(Enum):
    INITIAL = auto()
    TIRES_ANALYZED = auto()
    FUEL_ANALYZED = auto()
    WEATHER_ANALYZED = auto()
    DECISION_MADE = auto()

@dataclass
class CarStatus:
    """Represents the current state of the race car"""
    tire_temperature: float  # in Celsius
    tire_wear_percentage: float
    fuel_level: float  # in liters
    current_lap: int
    weather_condition: str = ""
    
    # Analysis results
    tire_status: str = ""
    fuel_status: str = ""
    weather_status: str = ""
    pit_decision: bool = False
    current_state: AnalysisState = AnalysisState.INITIAL

class KnowledgeSource(ABC):
    """Base class for all expert components"""
    @abstractmethod
    def can_contribute(self, blackboard: 'Blackboard') -> bool:
        pass

    @abstractmethod
    def contribute(self, blackboard: 'Blackboard') -> None:
        pass

class TireAnalyzer(KnowledgeSource):
    def can_contribute(self, blackboard: 'Blackboard') -> bool:
        return blackboard.car_status.current_state == AnalysisState.INITIAL

    def contribute(self, blackboard: 'Blackboard') -> None:
        status = blackboard.car_status
        
        # Analyze tire condition
        if status.tire_temperature > 100 or status.tire_wear_percentage > 75:
            status.tire_status = "Tires need replacement"
        else:
            status.tire_status = "Tires OK"
            
        status.current_state = AnalysisState.TIRES_ANALYZED

class FuelCalculator(KnowledgeSource):
    def can_contribute(self, blackboard: 'Blackboard') -> bool:
        return blackboard.car_status.current_state == AnalysisState.TIRES_ANALYZED

    def contribute(self, blackboard: 'Blackboard') -> None:
        status = blackboard.car_status
        
        # Calculate if current fuel is sufficient
        laps_remaining = 70 - status.current_lap
        fuel_needed = laps_remaining * 2.0  # Assume 2L per lap
        
        if status.fuel_level < fuel_needed:
            status.fuel_status = "Refueling needed"
        else:
            status.fuel_status = "Fuel level OK"
            
        status.current_state = AnalysisState.FUEL_ANALYZED

class WeatherMonitor(KnowledgeSource):
    def can_contribute(self, blackboard: 'Blackboard') -> bool:
        return blackboard.car_status.current_state == AnalysisState.FUEL_ANALYZED

    def contribute(self, blackboard: 'Blackboard') -> None:
        status = blackboard.car_status
        
        # Analyze weather conditions
        if status.weather_condition == "Rain":
            status.weather_status = "Rain detected - Consider wet tires"
        else:
            status.weather_status = "Weather OK"
            
        status.current_state = AnalysisState.WEATHER_ANALYZED

class Blackboard:
    """Central hub for storing the car status and analysis results"""
    def __init__(self, car_status: CarStatus):
        self.car_status = car_status

class RaceEngineer:
    """Controller that orchestrates the analysis process"""
    def __init__(self, blackboard: Blackboard):
        self.blackboard = blackboard
        self.knowledge_sources: List[KnowledgeSource] = [
            TireAnalyzer(),
            FuelCalculator(),
            WeatherMonitor()
        ]

    def analyze_pit_stop_need(self) -> None:
        """Main analysis loop"""
        for expert in self.knowledge_sources:
            if expert.can_contribute(self.blackboard):
                expert.contribute(self.blackboard)
        
        # Make final pit stop decision
        status = self.blackboard.car_status
        status.pit_decision = (
            "need" in status.tire_status.lower() or
            "need" in status.fuel_status.lower() or
            "rain" in status.weather_status.lower()
        )
        status.current_state = AnalysisState.DECISION_MADE

# USAGE EXAMPLE
# Create initial car status
car_status = CarStatus(
    tire_temperature = 105.0,
    tire_wear_percentage = 80.0,
    fuel_level = 50.0,
    current_lap = 30,
    weather_condition = "Rain"
)

# Initialize the blackboard
blackboard = Blackboard(car_status)

# Create and run the race engineer
engineer = RaceEngineer(blackboard)
engineer.analyze_pit_stop_need()

# Check results
print(f"Tire Analysis: {blackboard.car_status.tire_status}")
print(f"Fuel Analysis: {blackboard.car_status.fuel_status}")
print(f"Weather Analysis: {blackboard.car_status.weather_status}")
print(f"Pit Stop Needed: {blackboard.car_status.pit_decision}")

