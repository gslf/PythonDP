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