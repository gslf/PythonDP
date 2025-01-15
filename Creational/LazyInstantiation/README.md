# Lazy Instantiation in Python
Lazy Instantiation, also known as Lazy Loading or Lazy Initialization, is a design pattern that delays the creation of an object until the first time it's needed.

The core philosophy behind Lazy Instantiation aligns perfectly with the principle of **"don't pay for what you don't use"**. In modern applications, where resource management and performance are crucial, initializing objects only when necessary can significantly improve efficiency.

**The pattern consists of three main components:**

- A wrapper class that manages the lazy object
- The actual resource-intensive object
- A mechanism to check if the object has been instantiated

The wrapper class acts as a proxy, handling the instantiation logic and ensuring thread safety when necessary. It typically maintains a private reference to the actual object and a flag indicating whether the object has been instantiated.

![Lazy Instantiation Pattern Visual Representation](/Creational/LazyInstantiation/res/lazy_instantiation_visualization.png)

## Implementation
Let's consider a real-world scenario: a document processing application that can export files to different formats. The PDF export functionality requires loading heavy libraries and establishing complex configurations, but not every user will need PDF export capabilities in every session.

Instead of loading the PDF exporter during application startup, we can use Lazy Instantiation to create it only when a user actually requests a PDF export. This approach saves memory and reduces startup time for users who never export to PDF.

```python
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
```