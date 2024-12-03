# The Composite Design Pattern

The Composite Pattern  allows a diverse set of objects, with different internal complexities, to present a **unified interface** to clients. It's used when you want to be able to treat individual objects and groups of objects in the same way. By defining an interface for objects that can either be individual items or composites of items, you allow client code to interact with these elements without worrying about their internal structure.

In terms of code, think of a motorsport team. The team manager oversees different team members, such as drivers and mechanics. The drivers focus on racing, while the mechanics support the race. The key idea is that both an individual driver and the entire team can respond to a request like "prepare for the race," even though their roles and compositions are different.

![Composite Pattern Visual Representation](/Composite/res/composite_visualization.png)

## Implementation

The code example illustrates a motorsport team scenario using the Composite Design Pattern. It shows how we can represent both individual entities like drivers and mechanics (leaves) and larger groups like entire teams (composites) with a consistent interface. This means that individual team members and whole teams can be treated in the same way, allowing for easy management and flexible composition of race teams.

```python
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
```