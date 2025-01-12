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
