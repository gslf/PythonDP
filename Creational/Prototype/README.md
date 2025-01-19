# The prototype design pattern

The Prototype pattern is a creational design pattern that is used to create new objects by copying an existing object. In software engineering we must  This pattern is particularly useful when object creation is expensive or complex, allowing us to clone objects rather than create them from scratch. It emphasizes the idea of minimizing duplication of creation logic and promoting object reuse.

Consider a scenario in a game development environment. Imagine you need to spawn thousands of non-player characters (NPCs) that share similar attributes but have slight differences. Instead of creating each NPC from scratch, which could be resource-heavy and time-consuming, you create a prototype character with base attributes. You then clone this character, adjusting only what’s necessary for each instance. The prototype pattern offers an elegant way to manage such scenarios.

![Builder Pattern Visual Representation](/Creational/Builder/res/builder.png)

## Implementation

This is an easy implementation of the Prototype pattern:

```python
from abc import ABC, abstractmethod
import copy

# Base Prototype class
class Prototype(ABC):
    
    @abstractmethod
    def clone(self):
        pass

# A concrete implementation of Prototype
class Character(Prototype):
    def __init__(self, name, level, health):
        self.name = name
        self.level = level
        self.health = health

    def __str__(self):
        return f"Character({self.name}, Level: {self.level}, Health: {self.health})"

    # Implementing the clone method
    def clone(self):
        # Returning a deep copy to ensure no references are shared
        return copy.deepcopy(self)

# Client Code
if __name__ == "__main__":
    # Creating a prototype instance
    prototype_character = Character("Warrior", 1, 100)
    
    # Cloning the prototype
    cloned_character = prototype_character.clone()
    cloned_character.name = "Archer"  # Customizing the clone
    
    print("Original Prototype: ", prototype_character)
    print("Cloned Character: ", cloned_character)

```