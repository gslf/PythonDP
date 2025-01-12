# Template Design Pattern in Python
The Template Design Pattern represents a fundamental approach in object-oriented programming where a base class defines the skeleton of an algorithm, deferring some steps to subclasses. This pattern enables you to define the structure of an algorithm while allowing specific steps to be implemented differently by derived classes.

The philosophy behind this pattern lies in the "Don't Repeat Yourself" (DRY) principle and the "Hollywood Principle" - "don't call us, we'll call you." It promotes code reuse and maintains a consistent structure across various implementations while providing flexibility where needed. This approach is particularly valuable when you have multiple classes that share similar processes but differ in specific details.

The pattern consists of two main components:

- **Abstract Class (Template):** Defines the algorithm's structure and contains both concrete and abstract methods.
- **Concrete Classes:** Implement the abstract methods defined in the template while inheriting the fixed algorithm structure.

![Template Pattern Visualizatoin](/Behavioral/Template/res/template_visualization.png)


## Implementation

To understand this pattern, let's consider a real-world example: a document export system. Imagine you're building software that exports documents to different formats (PDF and HTML). The basic process remains the same: load content, format it, and save it. However, the specific formatting and saving steps differ for each format.

Here is the code:

```python
from abc import ABC, abstractmethod
from typing import List, Optional
from dataclasses import dataclass

@dataclass
class Document:
    """Represents a document with title and content"""
    title: str
    content: List[str]

class DocumentExporter(ABC):
    """Template class defining the document export algorithm"""
    
    def export_document(self, document: Document) -> bool:
        """
        Template method defining the algorithm structure
        Returns True if export was successful
        """
        # Common steps for all exporters
        content = self._load_content(document)
        if not content:
            return False
            
        formatted_content = self._format_content(content)
        success = self._save_content(formatted_content)
        
        if success:
            self._notify_completion(document.title)
        
        return success
    
    def _load_content(self, document: Document) -> Optional[List[str]]:
        """Common implementation for content loading"""
        if not document.content:
            print("Error: Empty document")
            return None
        return document.content
    
    @abstractmethod
    def _format_content(self, content: List[str]) -> str:
        """Each exporter must implement its formatting logic"""
        pass
    
    @abstractmethod
    def _save_content(self, formatted_content: str) -> bool:
        """Each exporter must implement its saving logic"""
        pass
    
    def _notify_completion(self, title: str) -> None:
        """Common implementation for completion notification"""
        print(f"Document '{title}' exported successfully")

class PDFExporter(DocumentExporter):
    """Concrete implementation for PDF export"""
    
    def _format_content(self, content: List[str]) -> str:
        # Simulating PDF-specific formatting
        return f"PDF Format:\n{''.join(f'- {line}\n' for line in content)}"
    
    def _save_content(self, formatted_content: str) -> bool:
        # Simulating saving as PDF
        print("Saving as PDF...")
        print(formatted_content)
        return True

class HTMLExporter(DocumentExporter):
    """Concrete implementation for HTML export"""
    
    def _format_content(self, content: List[str]) -> str:
        # Simulating HTML-specific formatting
        html_content = "<html><body>\n"
        for line in content:
            html_content += f"<p>{line}</p>\n"
        html_content += "</body></html>"
        return html_content
    
    def _save_content(self, formatted_content: str) -> bool:
        # Simulating saving as HTML
        print("Saving as HTML...")
        print(formatted_content)
        return True
    


    
# EXAMPLE USAGE

# Create a sample document
document = Document(
    title="Annual Report",
    content=[
        "Executive Summary",
        "Financial Results",
        "Future Outlook"
    ]
)

# Export using PDF format
print("\n=== PDF Export ===")
pdf_exporter = PDFExporter()
pdf_exporter.export_document(document)

# Export using HTML format
print("\n=== HTML Export ===")
html_exporter = HTMLExporter()
html_exporter.export_document(document)

```
