import time
import uuid
import traceback
from app.worker.celery_app import celery
from app.core.database import SessionLocal
from app.models.document import Document
from app.models.job import ProcessingJob
from app.services.rag import index_document

@celery.task(name="app.worker.tasks.process_document_task")
def process_document_task(document_id_str: str):
    document_id = uuid.UUID(document_id_str)
    db = SessionLocal()
    
    # 1. Fetch document record
    document = db.query(Document).filter(Document.id == document_id).first()
    if not document:
        print(f"Document with ID {document_id_str} not found in DB.")
        db.close()
        return False
    
    # 2. Update document state and init processing job
    document.status = "PROCESSING"
    
    from datetime import datetime
    job = ProcessingJob(
        document_id=document_id,
        status="RUNNING",
        started_at=datetime.utcnow()
    )
    db.add(job)
    db.commit()
    
    try:
        print(f"Starting ingestion pipeline for file: {document.file_name}")
        
        # 3. Call LlamaIndex ingestion pipeline
        total_pages, chunk_count = index_document(
            document_id=document.id,
            file_path=document.file_path,
            file_name=document.file_name
        )
        
        # 4. Success updates
        document.status = "INDEXED"
        document.total_pages = total_pages
        document.chunk_count = chunk_count
        
        job.status = "COMPLETED"
        job.completed_at = datetime.utcnow()
        db.commit()
        
        print(f"Successfully processed document: {document.file_name} (Pages: {total_pages}, Chunks: {chunk_count})")
        return True
        
    except Exception as e:
        error_msg = f"Error: {str(e)}\n{traceback.format_exc()}"
        print(f"Failed to ingest document {document.file_name}: {error_msg}")
        
        # 5. Rollback on failure, log logs
        db.rollback()
        
        document.status = "FAILED"
        job.status = "FAILED"
        job.completed_at = datetime.utcnow()
        job.error_message = error_msg[:1000] # Cap message length
        db.commit()
        return False
        
    finally:
        db.close()
