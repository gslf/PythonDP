from abc import ABC, abstractmethod
from datetime import datetime

# State Interface
class DocumentState(ABC):
    @abstractmethod
    def edit_content(self, document: 'Document', new_content: str) -> None:
        pass
    
    @abstractmethod
    def submit_for_review(self, document: 'Document') -> None:
        pass
    
    @abstractmethod
    def approve(self, document: 'Document') -> None:
        pass
    
    @abstractmethod
    def archive(self, document: 'Document') -> None:
        pass

# Concrete States
class DraftState(DocumentState):
    def edit_content(self, document: 'Document', new_content: str) -> None:
        document.content = new_content
        document.last_modified = datetime.now()
        print("Document content updated")
    
    def submit_for_review(self, document: 'Document') -> None:
        document.state = UnderReviewState()
        print("Document submitted for review")
    
    def approve(self, document: 'Document') -> None:
        print("Error: Cannot approve a draft document")
    
    def archive(self, document: 'Document') -> None:
        print("Error: Cannot archive a draft document")

class UnderReviewState(DocumentState):
    def edit_content(self, document: 'Document', new_content: str) -> None:
        print("Error: Cannot edit document under review")
    
    def submit_for_review(self, document: 'Document') -> None:
        print("Error: Document is already under review")
    
    def approve(self, document: 'Document') -> None:
        document.state = PublishedState()
        print("Document approved and published")
    
    def archive(self, document: 'Document') -> None:
        print("Error: Cannot archive document under review")

class PublishedState(DocumentState):
    def edit_content(self, document: 'Document', new_content: str) -> None:
        print("Error: Cannot edit published document")
    
    def submit_for_review(self, document: 'Document') -> None:
        print("Error: Cannot submit published document for review")
    
    def approve(self, document: 'Document') -> None:
        print("Error: Document is already published")
    
    def archive(self, document: 'Document') -> None:
        document.state = ArchivedState()
        print("Document archived")

class ArchivedState(DocumentState):
    def edit_content(self, document: 'Document', new_content: str) -> None:
        print("Error: Cannot edit archived document")
    
    def submit_for_review(self, document: 'Document') -> None:
        print("Error: Cannot submit archived document for review")
    
    def approve(self, document: 'Document') -> None:
        print("Error: Cannot approve archived document")
    
    def archive(self, document: 'Document') -> None:
        print("Error: Document is already archived")

# Context
class Document:
    def __init__(self, content: str):
        self.content: str = content
        self.state: DocumentState = DraftState()
        self.last_modified: datetime = datetime.now()
    
    def edit_content(self, new_content: str) -> None:
        self.state.edit_content(self, new_content)
    
    def submit_for_review(self) -> None:
        self.state.submit_for_review(self)
    
    def approve(self) -> None:
        self.state.approve(self)
    
    def archive(self) -> None:
        self.state.archive(self)




# EXAMPLE USAGE

# Create a new document in Draft state
doc = Document("Initial content")

# Demonstrate document lifecycle
print("\n--- Working with draft document ---")
doc.edit_content("Updated content")  # Works (Draft state allows editing)
doc.approve()  # Error (Can't approve draft directly)

print("\n--- Submitting for review ---")
doc.submit_for_review()  # Transitions to UnderReview state
doc.edit_content("Try to edit")  # Error (Can't edit while under review)

print("\n--- Approving document ---")
doc.approve()  # Transitions to Published state

print("\n--- Working with published document ---")
doc.edit_content("Try to edit published")  # Error (Can't edit published document)
doc.submit_for_review()  # Error (Can't review published document)

print("\n--- Archiving document ---")
doc.archive()  # Transitions to Archived state
doc.edit_content("Try to edit archived")  # Error (Can't edit archived document)