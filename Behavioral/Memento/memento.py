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


# Example usage

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