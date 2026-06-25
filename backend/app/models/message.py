import uuid
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, Text, func
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from app.core.database import Base

class Message(Base):
    __tablename__ = "messages"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    conversation_id = Column(UUID(as_uuid=True), ForeignKey("conversations.id", ondelete="CASCADE"), nullable=False)
    role = Column(String(20), nullable=False)  # "USER" or "ASSISTANT"
    content = Column(Text, nullable=False)
    retrieved_sources = Column(JSONB, nullable=True)  # List of dicts with doc_id, chunk_id, page_number, similarity, text
    token_count = Column(Integer, nullable=True)
    created_at = Column(DateTime, nullable=False, server_default=func.now())

    # Relationships
    conversation = relationship("Conversation", back_populates="messages")
    retrieval_logs = relationship("RetrievalLog", back_populates="message", cascade="all, delete-orphan")
    ai_response_logs = relationship("AIResponseLog", back_populates="message", cascade="all, delete-orphan")
