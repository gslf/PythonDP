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