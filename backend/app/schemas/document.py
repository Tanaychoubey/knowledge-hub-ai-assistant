from datetime import datetime
from typing import Optional
from uuid import UUID
from pydantic import BaseModel

class DocumentResponse(BaseModel):
    id: UUID
    file_name: str
    file_type: str
    file_size: int
    status: str
    total_pages: Optional[int] = None
    chunk_count: Optional[int] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
