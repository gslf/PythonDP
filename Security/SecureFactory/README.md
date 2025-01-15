# Secure Factory in Python
The Secure Factory pattern is an enhancement of the traditional Factory pattern, focusing on secure and controlled object instantiation. It ensures that objects are created following strict security protocols and validation rules, making it particularly valuable in systems where object creation must adhere to specific security requirements.

The pattern becomes essential in systems handling sensitive data, financial transactions, or any scenario where object creation must be tightly controlled. It consists of three main components:

- **The Secure Factory** serves as the main entry point for object creation, implementing security checks and validation logic. It acts as a gatekeeper, ensuring that all creation requests are legitimate and safe.

- **The Validation Handler** performs specific checks on creation parameters and context, verifying that all security requirements are met before object instantiation.

- **The Product** represents the actual object being created, which can only be instantiated through the Secure Factory after passing all security checks.

![Secure Factory Pattern Visual Representation](/Security/SecureFactory/res/secure_factory_visualization.png)

## Implementation
Consider a document management system for a legal firm. The system needs to create different types of legal documents while ensuring that only authorized users can create specific document types, and all documents are properly initialized with necessary security metadata.

In this scenario, a regular factory pattern would be insufficient as it wouldn't guarantee that documents are created with proper authorization and security controls. The Secure Factory pattern ensures that:

- Document creation requests are validated against user permissions
- Documents are properly tagged with creation metadata
- Sensitive content is properly initialized
- Document creation adheres to compliance requirements

```python
from datetime import datetime
from typing import Optional, Dict, Any
from dataclasses import dataclass
from enum import Enum
import hashlib

class DocumentType(Enum):
    CONTRACT = "contract"
    AGREEMENT = "agreement"
    AFFIDAVIT = "affidavit"

class SecurityLevel(Enum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3

@dataclass
class User:
    id: str
    security_clearance: SecurityLevel
    department: str

@dataclass
class Document:
    id: str
    type: DocumentType
    content: str
    created_by: str
    created_at: datetime
    security_hash: str
    metadata: Dict[str, Any]

class SecurityValidator:
    @staticmethod
    def validate_user_permissions(user: User, doc_type: DocumentType) -> bool:
        # Security validation logic
        if doc_type == DocumentType.AFFIDAVIT and user.security_clearance != SecurityLevel.HIGH:
            return False
        return True

    @staticmethod
    def generate_security_hash(content: str, user_id: str) -> str:
        return hashlib.sha256(f"{content}{user_id}".encode()).hexdigest()

class SecureDocumentFactory:
    def __init__(self):
        self.validator = SecurityValidator()

    def create_document(
        self,
        doc_type: DocumentType,
        content: str,
        user: User,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Optional[Document]:
        # Validate user permissions
        if not self.validator.validate_user_permissions(user, doc_type):
            return None

        # Generate security hash
        security_hash = self.validator.generate_security_hash(content, user.id)

        # Create document with security controls
        return Document(
            id=f"DOC_{datetime.now().timestamp()}",
            type=doc_type,
            content=content,
            created_by=user.id,
            created_at=datetime.now(),
            security_hash=security_hash,
            metadata=metadata or {}
        )

######################################
# Usage Example

# Create a user and factory
# Create users with different security clearances
high_clearance_user = User(
    id="USR123", 
    security_clearance=SecurityLevel.HIGH, 
    department="Legal"
)

low_clearance_user = User(
    id="USR456", 
    security_clearance=SecurityLevel.LOW, 
    department="Legal"
)

factory = SecureDocumentFactory()

# Successful creation - High clearance user creating an affidavit
document = factory.create_document(
    doc_type=DocumentType.AFFIDAVIT,
    content="This is a confidential affidavit",
    user=high_clearance_user,
    metadata={"jurisdiction": "New York", "case_number": "123-456"}
)

if document:
    print(f"Success: Document created with ID: {document.id} - Hash: {document.security_hash}")
else:
    print("Error: Document creation failed")

# Failed creation - Low clearance user attempting to create an affidavit
document = factory.create_document(
    doc_type=DocumentType.AFFIDAVIT,
    content="This is an unauthorized affidavit attempt",
    user=low_clearance_user,
    metadata={"jurisdiction": "New York", "case_number": "789-012"}
)

if document:
    print(f"Success: Document created with ID: {document.id} - Hash: {document.security_hash}")
else:
    print("Error: Document creation failed - Insufficient security clearance")
```