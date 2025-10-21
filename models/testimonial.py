from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
import uuid

class Testimonial(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    text: str
    author: str
    role: str
    company: Optional[str] = None
    avatar: Optional[str] = None
    rating: Optional[int] = Field(default=5, ge=1, le=5)
    is_active: bool = True
    order: int = 0
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class TestimonialCreate(BaseModel):
    text: str
    author: str
    role: str
    company: Optional[str] = None
    avatar: Optional[str] = None
    rating: Optional[int] = Field(default=5, ge=1, le=5)
    order: Optional[int] = 0

class TestimonialResponse(BaseModel):
    id: str
    text: str
    author: str
    role: str
    company: Optional[str]
    avatar: Optional[str]
    rating: int
