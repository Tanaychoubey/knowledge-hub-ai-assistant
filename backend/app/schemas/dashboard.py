from datetime import datetime
from typing import Optional
from uuid import UUID
from pydantic import BaseModel

class SystemMetrics(BaseModel):
    total_documents: int
    total_chunks: int
    total_conversations: int
    average_latency_ms: int

class JobResponse(BaseModel):
    id: UUID
    document_id: UUID
    document_name: str
    status: str
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    error_message: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True
