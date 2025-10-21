from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime
from enum import Enum
import uuid

class ContactType(str, Enum):
    SUPPORT = "support"
    SALES = "sales"
    GENERAL = "general"

class ContactStatus(str, Enum):
    NEW = "new"
    IN_PROGRESS = "in-progress"
    RESOLVED = "resolved"

class Contact(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    email: EmailStr
    subject: Optional[str] = None
    message: str
    type: ContactType = ContactType.GENERAL
    status: ContactStatus = ContactStatus.NEW
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class ContactCreate(BaseModel):
    name: str
    email: EmailStr
    subject: Optional[str] = None
    message: str
    type: ContactType = ContactType.GENERAL

class ContactResponse(BaseModel):
    id: str
    name: str
    email: str
    subject: Optional[str]
    message: str
    type: ContactType
    status: ContactStatus
    created_at: datetime
