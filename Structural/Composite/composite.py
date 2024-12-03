from abc import ABC, abstractmethod
from typing import List

# Component
class TeamComponent(ABC):
    @abstractmethod
    def race(self) -> None:
        pass

# Leaf
class Driver(TeamComponent):
    def __init__(self, name: str) -> None:
        self.name = name

    def race(self) -> None:
        print(f"Driver {self.name} is racing")

# Leaf
class Mechanic(TeamComponent):
    def __init__(self, name: str) -> None:
        self.name = name

    def race(self) -> None:
        print(f"Mechanic {self.name} is supporting the race")

# Composite
class Team(TeamComponent):
    def __init__(self, name: str) -> None:
        self.name = name
        self._members: List[TeamComponent] = []

    def add(self, member: TeamComponent) -> None:
        self._members.append(member)

    def remove(self, member: TeamComponent) -> None:
        self._members.remove(member)

    def race(self) -> None:
        print(f"Team {self.name} is preparing for the race with the following members:")
        for member in self._members:
            member.race()

# Client code
def main() -> None:
    # Creating individual team members
    driver1 = Driver("Lewis Hamilton")
    driver2 = Driver("Max Verstappen")
    mechanic1 = Mechanic("John Doe")
    mechanic2 = Mechanic("Jane Smith")

    # Creating a team
    team1 = Team("Red Bull Racing")
    team1.add(driver1)
    team1.add(mechanic1)

    # Creating another team
    team2 = Team("Mercedes AMG")
    team2.add(driver2)
    team2.add(mechanic2)
    team2.add(team1)

    # Racing
    print("Team 1:")
    team1.race()
    print("\nTeam 2:")
    team2.race()

if __name__ == "__main__":
    main()