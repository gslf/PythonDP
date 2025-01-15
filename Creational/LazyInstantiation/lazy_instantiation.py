from typing import Optional
from dataclasses import dataclass
from time import sleep

@dataclass
class PDFConfiguration:
    """Represents heavy PDF configuration settings"""
    resolution: int
    compression_level: int
    encryption_enabled: bool

class PDFExporter:
    """Resource-intensive PDF export functionality"""
    
    def __init__(self) -> None:
        # Simulate heavy initialization
        sleep(2)  # Represents time-consuming setup
        self.config = PDFConfiguration(
            resolution=300,
            compression_level=9,
            encryption_enabled=True
        )
    
    def export(self, content: str) -> str:
        return f"PDF exported: {content}"

class DocumentManager:
    """Wrapper class implementing lazy instantiation"""
    
    def __init__(self) -> None:
        self._pdf_exporter: Optional[PDFExporter] = None
    
    @property
    def pdf_exporter(self) -> PDFExporter:
        """Lazy getter for PDFExporter instance"""
        if self._pdf_exporter is None:
            print("Initializing PDF exporter...")
            self._pdf_exporter = PDFExporter()
        return self._pdf_exporter
    
    def export_to_pdf(self, content: str) -> str:
        """Method that triggers lazy instantiation"""
        return self.pdf_exporter.export(content)
    
    def export_to_txt(self, content: str) -> str:
        """Method that doesn't need the heavy PDF exporter"""
        return f"TXT exported: {content}"

####################################
# Usage Example
doc_manager = DocumentManager()

# This operation is fast as it doesn't need the PDF exporter
print(doc_manager.export_to_txt("Hello World"))

# The PDF exporter is created only when first needed
print(doc_manager.export_to_pdf("Hello World"))

# Subsequent PDF exports reuse the existing instance
print(doc_manager.export_to_pdf("Another document"))