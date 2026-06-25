import uuid
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, Text, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.core.database import Base

class RetrievalLog(Base):
    __tablename__ = "retrieval_logs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    message_id = Column(UUID(as_uuid=True), ForeignKey("messages.id", ondelete="CASCADE"), nullable=False)
    query_text = Column(Text, nullable=False)
    top_k = Column(Integer, nullable=False, default=5)
    retrieval_latency_ms = Column(Integer, nullable=False)
    created_at = Column(DateTime, nullable=False, server_default=func.now())

    # Relationships
    message = relationship("Message", back_populates="retrieval_logs")

class AIResponseLog(Base):
    __tablename__ = "ai_response_logs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    message_id = Column(UUID(as_uuid=True), ForeignKey("messages.id", ondelete="CASCADE"), nullable=False)
    model_name = Column(String(100), nullable=False)
    prompt_tokens = Column(Integer, nullable=True)
    completion_tokens = Column(Integer, nullable=True)
    generation_time_ms = Column(Integer, nullable=False)
    created_at = Column(DateTime, nullable=False, server_default=func.now())

    # Relationships
    message = relationship("Message", back_populates="ai_response_logs")
