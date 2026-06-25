from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.api.deps import get_current_user, get_current_active_admin
from app.models.user import User
from app.models.document import Document
from app.models.job import ProcessingJob
from app.models.conversation import Conversation
from app.models.logs import RetrievalLog
from app.schemas.dashboard import SystemMetrics, JobResponse

router = APIRouter()

@router.get("/metrics", response_model=SystemMetrics)
def get_system_metrics(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Total documents uploaded
    total_docs = db.query(Document).count()
    
    # Total chunks parsed in the system (sum of Document.chunk_count)
    total_chunks = db.query(func.sum(Document.chunk_count)).scalar() or 0
    
    # Total conversations created
    total_convs = db.query(Conversation).count()
    
    # Average retrieval latency
    avg_latency = db.query(func.avg(RetrievalLog.retrieval_latency_ms)).scalar() or 0
    
    return {
        "total_documents": total_docs,
        "total_chunks": int(total_chunks),
        "total_conversations": total_convs,
        "average_latency_ms": int(avg_latency)
    }

@router.get("/jobs", response_model=List[JobResponse])
def list_processing_jobs(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_admin)
):
    # Retrieve jobs joined with document names to show them in the admin dashboard
    results = db.query(
        ProcessingJob.id,
        ProcessingJob.document_id,
        ProcessingJob.status,
        ProcessingJob.started_at,
        ProcessingJob.completed_at,
        ProcessingJob.error_message,
        ProcessingJob.created_at,
        Document.file_name
    ).join(Document, ProcessingJob.document_id == Document.id).order_by(
        ProcessingJob.created_at.desc()
    ).limit(50).all()
    
    jobs = []
    for row in results:
        jobs.append({
            "id": row.id,
            "document_id": row.document_id,
            "document_name": row.file_name,
            "status": row.status,
            "started_at": row.started_at,
            "completed_at": row.completed_at,
            "error_message": row.error_message,
            "created_at": row.created_at
        })
        
    return jobs
