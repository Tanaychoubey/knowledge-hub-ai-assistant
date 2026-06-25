from datetime import datetime
from typing import List, Optional, Any
from uuid import UUID
from pydantic import BaseModel

class MessageResponse(BaseModel):
    id: UUID
    role: str
    content: str
    retrieved_sources: Optional[Any] = None
    created_at: datetime

    class Config:
        from_attributes = True

class ConversationResponse(BaseModel):
    id: UUID
    title: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class ConversationDetailResponse(ConversationResponse):
    messages: List[MessageResponse] = []
