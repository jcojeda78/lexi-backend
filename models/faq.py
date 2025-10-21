from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
import uuid

class FAQ(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    question: str
    answer: str
    category: Optional[str] = "general"
    order: int = 0
    is_active: bool = True
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class FAQCreate(BaseModel):
    question: str
    answer: str
    category: Optional[str] = "general"
    order: Optional[int] = 0

class FAQResponse(BaseModel):
    id: str
    question: str
    answer: str
    category: Optional[str]
