# The Flyweight Design Pattern

The Flyweight pattern is a structural design pattern that helps reduce the memory footprint of applications by **sharing data across multiple similar objects**. It allows the creation of a large number of fine-grained objects efficiently, without duplicating shared state. This pattern is particularly useful when your program needs to instantiate many similar objects, such as GUI components, characters in a game, or even data entries in a big dataset.

![Facade Pattern Visual Representation](/Facade/res/facade_visualization.png)

For those who prefer a visual approach, imagine the Flyweight pattern as similar to an art studio painting multiple identical canvases with slight variations. Instead of creating an entire new painting for each canvas from scratch, the artist uses stencils for the common parts and applies unique touches only where needed.


# How it work

The Flyweight pattern separates an object's state into **two categories**, which helps optimize memory usage by differentiating between what can be shared and what cannot. This separation allows for effective reuse and avoids redundant data allocation. 

This are the flyweight state categories:

1. Intrinsic State: The invariant, shared state that can be reused among many instances.
2. Extrinsic State: The context-specific state that needs to be passed to the object as required.

## Implementation

This implementation demonstrates the use of the Flyweight pattern in a video game development context. The goal is to create multiple instances of the Character class while sharing the same intrinsic state for characters that have identical attributes. This approach optimizes memory usage by reducing redundant data, especially when dealing with a large number of similar game entities. Here's how we achieve it:

```python
class CharacterType:
    """
    The flyweight class contains a portion of the state of a character.
    These fields store values that are unique for each particular character.
    The sprite, animations, and abilities shared between many characters are stored here.
    This approach saves memory by sharing common aspects.
    """

    def __init__(self, name, sprite, abilities):
        self.name = name
        self.sprite = sprite
        self.abilities = abilities

    def draw(self, canvas, x, y):
        print(f"Draw character in position {x}, {y}")

class CharacterFactory:
    """
    Flyweight factory that decides whether to reuse an existing CharacterType or create a new one.
    """
    character_types = []

    @staticmethod
    def get_character_type(name, sprite, abilities):
        """
        Get a character type. Reuse an existing one if available, otherwise create a new one.
        """
        for character_type in CharacterFactory.character_types:
            if (character_type.name == name and 
                character_type.sprite == sprite and 
                character_type.abilities == abilities):
                return character_type
        
        new_type = CharacterType(name, sprite, abilities)
        CharacterFactory.character_types.append(new_type)
        return new_type

class Character:
    """
    The contextual object that contains the extrinsic part of the character state.
    An application can create many of these since they are small: coordinates, health,
    experience, and one reference field.  
    """
    def __init__(self, x, y, health, experience, character_type):

        self.x = x
        self.y = y
        self.health = health
        self.experience = experience
        self.character_type = character_type

    def draw(self, canvas):
        """
        Draw the character on the canvas.
        """
        self.character_type.draw(canvas, self.x, self.y)

if __name__ == "__main__":
    # Create a mock canvas object for demonstration purposes.
    canvas = "CanvasMock"

    print("Spawn some characters and draw them.")
    character1_type = CharacterFactory.get_character_type("Knight", "knight_sprite.png", ["Slash", "Block"])
    character1 = Character(10, 20, 100, 10, character1_type)
    character1.draw(canvas)

    character2_type = CharacterFactory.get_character_type("Archer", "archer_sprite.png", ["Shoot", "Dodge"])
    character2 = Character(30, 40, 80, 15, character2_type)
    character2.draw(canvas)

    print("\nSpawn and draw another knight (which should reuse the existing character type).")
    character3_type = CharacterFactory.get_character_type("Knight", "knight_sprite.png", ["Slash", "Block"])
    character3 = Character(50, 60, 120, 20, character3_type)
    character3.draw(canvas)
```