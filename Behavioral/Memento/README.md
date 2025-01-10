# Memento Design Pattern in Python

The Memento design pattern is a behavioral pattern that provides a mechanism to capture and externalize an object's internal state, allowing it to be restored to this state later. This pattern implements an "undo" mechanism without violating encapsulation, meaning that the object's internal details remain hidden from the outside world.

The pattern consists of three main components working together:

- **Originator:** The object whose state needs to be saved and restored
- **Memento:** A state holder that stores the Originator's internal state
- **Caretaker:** Manages and safekeeps the Mementos without modifying their content

The Originator creates a Memento containing a snapshot of its current state. Later, this Memento can be used to restore the Originator to its previous state. The Caretaker is responsible for the Memento's safekeeping and never operates on or examines the contents of a Memento.

![Memento Pattern Visual Representation](/Behavioral/Memento/res/memento_visualization.png)

## Implementation

Consider a document editor where users can type text and perform formatting operations. Users expect to undo their changes when they make mistakes. The document, referred to as "Originator", encompasses both text and formatting information. Each time the user makes a change, a snapshot, known as the Memento, is created to capture the document's current state. The editor's undo system, identified as the Caretaker, is responsible for storing these snapshots. When the "undo" operation is fired, the editor retrieves the most recently stored snapshot, restoring the document to its previous state. 

```python
from dataclasses import dataclass
from typing import List
from datetime import datetime


@dataclass
class DocumentState:
    """Memento class that stores the document state"""
    content: str
    formatting: dict
    cursor_position: int
    timestamp: datetime


class Document:
    """Originator class representing a text document"""
    
    def __init__(self) -> None:
        self.content: str = ""
        self.formatting: dict = {}
        self.cursor_position: int = 0
    
    def type(self, text: str) -> None:
        """Add text at current cursor position"""
        self.content = (
            self.content[:self.cursor_position] +
            text +
            self.content[self.cursor_position:]
        )
        self.cursor_position += len(text)
    
    def apply_formatting(self, start: int, end: int, format_type: str) -> None:
        """Apply formatting to selected text range"""
        self.formatting[(start, end)] = format_type
    
    def create_snapshot(self) -> DocumentState:
        """Creates a memento containing the current state"""
        return DocumentState(
            content=self.content,
            formatting=self.formatting.copy(),
            cursor_position=self.cursor_position,
            timestamp=datetime.now()
        )
    
    def restore_from_snapshot(self, snapshot: DocumentState) -> None:
        """Restores state from a memento"""
        self.content = snapshot.content
        self.formatting = snapshot.formatting.copy()
        self.cursor_position = snapshot.cursor_position


class DocumentManager:
    """Caretaker class that manages document history"""
    
    def __init__(self, document: Document) -> None:
        self.document: Document = document
        self.history: List[DocumentState] = []
    
    def save(self) -> None:
        """Saves current document state"""
        self.history.append(self.document.create_snapshot())
    
    def undo(self) -> bool:
        """Restores the previous state if available"""
        if not self.history:
            return False
        
        previous_state = self.history.pop()
        self.document.restore_from_snapshot(previous_state)
        return True


# EXAMPLE USAGE

# Create document and its manager
doc = Document()
manager = DocumentManager(doc)

# Type some text and save state
doc.type("Hello ")
manager.save()

# Add more text and apply formatting
doc.type("world!")
doc.apply_formatting(0, 5, "bold")
manager.save()

# Make a change we might want to undo
doc.type(" How are you?")

# Demonstrate undo functionality
print(f"Current content: {doc.content}")  # Hello world! How are you?
manager.undo()
print(f"After first undo: {doc.content}")  # Hello world!
manager.undo()
print(f"After second undo: {doc.content}")  # Hello
```