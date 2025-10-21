from pydantic import BaseModel, EmailStr, Field
from typing import Optional, Dict, Any
from datetime import datetime
from enum import Enum
import uuid

class LeadStatus(str, Enum):
    NEW = "new"
    CONTACTED = "contacted"
    CONVERTED = "converted"
    LOST = "lost"

class Lead(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    email: EmailStr
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    company: Optional[str] = None
    phone: Optional[str] = None
    website: Optional[str] = None
    source: str  # 'hero', 'pricing', 'stats', etc.
    utm: Optional[Dict[str, Any]] = {}
    status: LeadStatus = LeadStatus.NEW
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class LeadCreate(BaseModel):
    email: EmailStr
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    company: Optional[str] = None
    phone: Optional[str] = None
    website: Optional[str] = None
    source: str = "unknown"
    utm: Optional[Dict[str, Any]] = {}

class LeadResponse(BaseModel):
    id: str
    email: str
    first_name: Optional[str]
    last_name: Optional[str]
    company: Optional[str]
    source: str
    status: LeadStatus
    created_at: datetime
