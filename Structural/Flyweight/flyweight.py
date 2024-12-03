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