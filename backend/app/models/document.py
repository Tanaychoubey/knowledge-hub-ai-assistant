import uuid
from sqlalchemy import Column, String, Integer, BigInteger, DateTime, ForeignKey, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.core.database import Base

class Document(Base):
    __tablename__ = "documents"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    file_name = Column(String(255), nullable=False)
    file_path = Column(String, nullable=False)
    file_type = Column(String(20), nullable=False)
    file_size = Column(BigInteger, nullable=False)
    status = Column(String(50), nullable=False, default="UPLOADED")  # "UPLOADED", "PROCESSING", "INDEXED", "FAILED"
    uploaded_by = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    total_pages = Column(Integer, nullable=True)
    chunk_count = Column(Integer, nullable=True)
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    updated_at = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())

    # Relationships
    uploader = relationship("User", back_populates="documents")
    processing_jobs = relationship("ProcessingJob", back_populates="document", cascade="all, delete-orphan")
